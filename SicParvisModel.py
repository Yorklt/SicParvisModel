import os
import bpy
import bpy_extras

bl_info = {
    "name": "Sic Parvis Model",
    "author": "Pon Pon Games",
    "version": (1, 0),
    "blender": (4, 1, 1),
    "location": "File > Export",
    "description": "Export FBX files for specific RPG dev kit",
    "warning": "Not enough debugging. This addon can cause crashes.",
    "doc_url": "",
    "tracker_url": "",
    "category": "Import-Export",
    }

# Log
# 0: Warn and Error
# 1: Debug
# 2: Debug (Noisy)
def print_log(text, level):
    level_max = 0
    if level <= level_max:
        print(text)

# 制御オペレータ
# 通常はbpy.types.Operatorだけを継承しますが、ここではExportHelperも継承します。
# invoke関数で標準のファイル選択メニューを出してくれます。
class UsualFBXExporter_OT_Exporter(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    # これでbpy.ops.usualfbxexporter.exporterでアクセス可能になります。
    bl_idname = "usualfbxexporter.exporter"
    bl_label = "Export FBX"
    bl_options = {'UNDO', 'PRESET'}

    # 処理の実行可否判定の定義です。
    # Objectモードのときだけ実行可能です。
    @classmethod
    def poll(self, context):
        return context.mode == 'OBJECT'

    # ExportHelperで必須の定義
    filename_ext = ""

    # ExportHelperが使用するプロパティ
    filter_glob: bpy.props.StringProperty(
            default = "*.fbx",
            options = {'HIDDEN'},
            maxlen = 255,
            )

    # 出力設定
    prop_separate: bpy.props.BoolProperty(
        name = "アクションは別のFBXで出力",
        description = "オブジェクトのFBXとアクションのFBXを別々に出力します。",
        default = True,
    )

    # 出力設定
    prop_collect: bpy.props.BoolProperty(
        name = "パーツを変えて複数出力",
        description = "コレクションごとに複数FBXを出力します。<指定ファイル名+_+コレクション名>.fbxで出力します。",
        default = False,
    )

    # 出力設定
    prop_anim_suffix: bpy.props.StringProperty(
        name = "接尾辞",
        description = "アクションだけのFBXは名前の後ろにこの接尾辞を付けます。（例: MyChar_Anim.fbx）。",
        default = "_Anim",
    )

    # 出力設定
    prop_scale: bpy.props.FloatProperty(
        name = "スケール",
        description = "全体のスケールです。",
        default = 1.0,
        min = 0.0001,
        max = 10000.0
    )

    # 出力設定
    prop_ignore: bpy.props.BoolProperty(
        name = "特定接頭辞で始まるオブジェクトを除外",
        description = "特定の名前で始まるオブジェクトを出力から除外します。ダミーオブジェクトなど。",
        default = True,
    )

    # 出力設定
    prop_ignore_prefix: bpy.props.StringProperty(
        name = "接頭辞",
        description = "この名前で始まるオブジェクトを除外します。",
        default = "_",
    )

    # ファイル選択ダイアログの右側に描かれる内容
    def draw(self, context):

        box: bpy.types.UILayout = self.layout.box()
        box.label(text = "出力設定")
        box.label(text = "")
        box.label(text = "FBX出力方法")
        box.prop(self, "prop_separate")
        box.prop(self, "prop_collect")
        box.label(text = "アクションファイル接尾辞")
        box.prop(self, "prop_anim_suffix")
        box.label(text = "")
        box.label(text = "スケール")
        box.prop(self, "prop_scale")
        box.label(text = "")
        box.prop(self, "prop_ignore")
        box.label(text = "除外オブジェクト接頭辞")
        box.prop(self, "prop_ignore_prefix")

    # 出力実行
    def exec_export(self, target_filepath: str, scale: float, bake_anim: bool, ):
    
        # アニメーションの簡略化設定
        # （0にするとスムーズになりますがファイルサイズが大きくなります）
        bake_anim_simplify_factor: float = 1.0

        # 標準エクスポーターの呼び出し
        bpy.ops.export_scene.fbx(
            filepath = target_filepath, # not default
            check_existing = True,
            filter_glob = ".fbx",
            use_selection = True, # not default
            use_visible = False,
            use_active_collection = False,
            global_scale = scale, # not default
            apply_unit_scale = True,
            apply_scale_options = "FBX_SCALE_NONE",
            use_space_transform = True,
            bake_space_transform = False,
            object_types = {"ARMATURE", "EMPTY", "MESH"}, # not default
            use_mesh_modifiers = True,
            mesh_smooth_type = "OFF",
            use_subsurf = False,
            use_mesh_edges = False,
            use_tspace = False,
            use_triangles = False,
            use_custom_props = False,
            add_leaf_bones = True,
            primary_bone_axis = "Y",
            secondary_bone_axis = "X",
            use_armature_deform_only = False,
            armature_nodetype = "NULL",
            bake_anim = bake_anim, # not default
            bake_anim_use_all_bones = True,
            bake_anim_use_nla_strips = False, # not default
            bake_anim_use_all_actions = True,
            bake_anim_force_startend_keying = True,
            bake_anim_step = 1.0,
            bake_anim_simplify_factor = bake_anim_simplify_factor, # not default,
            path_mode = "AUTO",
            embed_textures = False,
            batch_mode = "OFF",
            use_batch_own_dir = True,
            use_metadata = True,
            axis_forward = "-Z",
            axis_up = "Y"
            )

    # 出力実行ボタンを押した時の動作
    def execute(self, context):
        
        # フォルダパス
        folder_path = os.path.dirname(self.filepath)

        # ファイル名（拡張子無し）
        filename_no_ext = os.path.splitext(os.path.basename(self.filepath))[0]
        
        # 現在のフレームを0にする
        bpy.context.scene.frame_current = 0

        # スケール
        scale: float = self.prop_scale

        # シーン全体モード
        if self.prop_collect == False:
            # フルパスの生成
            filename: str = filename_no_ext + ".fbx"
            target_filepath = os.path.join(folder_path, filename)

            # すべてのオブジェクトを選択
            # hide_viewportはbpy.data.objectsのイテレーション中に使うとクラッシュするので、
            # オブジェクト名を介してアクセスする。
            obj_names = [obj.name for obj in bpy.data.objects]
            for obj_name in obj_names:
                object = bpy.data.objects[obj_name]
                object.hide_viewport = False
                object.hide_set(False)
                object.hide_select = False
                object.select_set(True)

            # 除外オブジェクトを選択解除
            if self.prop_ignore == True:
                for object in bpy.data.objects:
                    obj_name: str = object.name
                    if obj_name[:1] == self.prop_ignore_prefix:
                        object.select_set(False)

            # アクション同梱ならベイクする
            bake_anim: bool = False
            if self.prop_separate == False:
                bake_anim = True

            # 出力実行
            self.exec_export(
                target_filepath = target_filepath,
                scale = scale,
                bake_anim = bake_anim
                )

        # コレクション別モード
        if self.prop_collect == True:
            collect_names = [collect.name for collect in bpy.data.collections]
            for collect_name in collect_names:
                collection = bpy.data.collections[collect_name]

                # フルパスの生成
                filename: str = filename_no_ext + "_" + collection.name + ".fbx"
                target_filepath = os.path.join(folder_path, filename)

                # すべてのオブジェクトを選択解除
                for object in bpy.data.objects:
                    object.select_set(False)

                # コレクションをビューポート有効にセット
                collection.hide_viewport = False

                # コレクション内ののオブジェクトを選択
                obj_names = [obj.name for obj in collection.all_objects]
                for obj_name in obj_names:
                    object = bpy.data.objects[obj_name]
                    object.hide_viewport = False
                    object.hide_set(False)
                    object.hide_select = False
                    object.select_set(True)

                # 除外オブジェクトを選択解除
                if self.prop_ignore == True:
                    for object in bpy.data.objects:
                        obj_name: str = object.name
                        if obj_name[:1] == self.prop_ignore_prefix:
                            object.select_set(False)

                # アクション同梱ならベイクする
                bake_anim: bool = False
                if self.prop_separate == False:
                    bake_anim = True

                # 出力実行
                self.exec_export(
                    target_filepath = target_filepath,
                    scale = scale,
                    bake_anim = bake_anim
                    )

        # アクションFBXの出力
        if self.prop_separate == True:
            # フルパスの生成
            filename: str = filename_no_ext + self.prop_anim_suffix + ".fbx"
            target_filepath = os.path.join(folder_path, filename)

            # すべてのオブジェクトを選択解除
            for object in bpy.data.objects:
                object.select_set(False)

            # アーマチュアだけを選択
            obj_names = [obj.name for obj in bpy.data.objects]
            for obj_name in obj_names:
                object = bpy.data.objects[obj_name]
                if (object.type == "ARMATURE"):
                    object.hide_viewport = False
                    object.hide_set(False)
                    object.hide_select = False
                    object.select_set(True)

            # 出力実行
            self.exec_export(
                target_filepath = target_filepath,
                scale = scale,
                bake_anim = True
                )

        return {"FINISHED"}

# メニューに項目を追加
def add_item_to_menu(self, context):
    self.layout.operator(UsualFBXExporter_OT_Exporter.bl_idname, text="FBX for RPG kit (.fbx)")

# アドオンを有効にしたときにBlenderから呼ばれます。
# このとき、bpy.dataとbpy.contextにアクセス不可。
def register():
    print_log("register is called.", 1)
    bpy.utils.register_class(UsualFBXExporter_OT_Exporter)
    bpy.types.TOPBAR_MT_file_export.append(add_item_to_menu)

# アドオンを無効にしたときにBlenderから呼ばれます。
# このとき、bpy.dataとbpy.contextにアクセス不可。
def unregister():
    print_log("unregister is called", 1)
    bpy.types.TOPBAR_MT_file_export.remove(add_item_to_menu)
    bpy.utils.unregister_class(UsualFBXExporter_OT_Exporter)

# Blenderのテキストエディタで呼んだときの処理（デバッグ用）
if __name__ == "__main__":
    print_log("Usual FBX Exporter is called from main", 1)
    register()
    #unregister()


