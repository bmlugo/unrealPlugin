from unreal import (AssetToolsHelpers, EditorAssetLibrary, AssetTools, Material, MaterialFactoryNew, MaterialEditingLibrary, MaterialExpressionTextureSampleParameter2D as TexSample2D, MaterialProperty, AssetImportTask, FbxImportUI )

import os

class UnrealUtility:
    def __init__(self):
        self.substanceRootDir='/game/Substance'
        self.substanceBaseMatName = 'M_SubstanceBase'
        self.substanceBaseMatPath = self.substanceRootDir + self.substanceBaseMatName
        self.substanceTempFolder='/game/Substance/temp'
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetallic = "OcclusionRoughnessMetallic"

    def GetAssetTools(self)->AssetTools:
        return AssetToolsHelpers.get_asset_tools()
    
    def ImportFromDir(self):
        for file in os.listdir(dir):
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(dir, file))

    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")
        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = '/game/' + meshName
        importTask.automated=True
        importTask.save=True

        fbxImportOption = FbxImportUI()
        fbxImportOption.import_mesh=True
        fbxImportOption.import_as_skeletal=False
        fbxImportOption.import_materials=False
        fbxImportOption.static_mesh_import_data.combine_meshes=True
        importTask.options = fbxImportOption

        self.GetAssetTools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]


    def FindOrBuildBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath):
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)
        
        baseMat = self.GetAssetTools().create_asset(self.substanceBaseMatName, self.substanceRootDir, Material, MaterialFactoryNew())
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0 )
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)

        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallic)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC)

        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat
