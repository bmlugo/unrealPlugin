from unreal import (AssetToolsHelpers, EditorAssetLibrary, AssetTools, Material, MaterialFactoryNew, MaterialEditingLibrary, MaterialExpressionTextureSampleParameter2D as TexSample2D, MaterialProperty, AssetImportTask, FbxImportUI ) #imports Unreal Engine classes and functions

import os #imports file directory information

class UnrealUtility: #defines a class for asset import and material creation tasks in Unreal Engine
    def __init__(self): #initializes the class with default paths and material parameters

        #sets up paths and parameter names for Substances Painter materials and textures
        self.substanceRootDir='/game/Substance'
        self.substanceBaseMatName = 'M_SubstanceBase'
        self.substanceBaseMatPath = self.substanceRootDir + self.substanceBaseMatName
        self.substanceTempFolder='/game/Substance/temp'
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetallic = "OcclusionRoughnessMetallic"

    def GetAssetTools(self)->AssetTools: #defines a method to get the GetAssetTools instance
        return AssetToolsHelpers.get_asset_tools()

    def ImportFromDir(self): #iterates through files in whatever the specified directory is and imports whatever .fbx files it finds in them
        for file in os.listdir(dir):
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(dir, file))

    def LoadMeshFromPath(self, meshPath): #defines a method to load a mesh from whatever path is given
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "") # extracts the mesh name by removing the .fbx extension from the overall file name

        #creates an import task for the mesh file that specify import settings
        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = '/game/' + meshName
        importTask.automated=True
        importTask.save=True

        #configures import options for the fbx file
        fbxImportOption = FbxImportUI()
        fbxImportOption.import_mesh=True
        fbxImportOption.import_as_skeletal=False
        fbxImportOption.import_materials=False
        fbxImportOption.static_mesh_import_data.combine_meshes=True
        importTask.options = fbxImportOption

        self.GetAssetTools().import_asset_tasks([importTask]) #executes the import task using AssetTools and returns the imported object
        return importTask.get_objects()[0]


    def FindOrBuildBaseMaterial(self): #defines a method to find an existing base material or create a new one
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath): #checks if the base material exists and will load and return it if it does
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)

        baseMat = self.GetAssetTools().create_asset(self.substanceBaseMatName, self.substanceRootDir, Material, MaterialFactoryNew()) #creates a new material asset in the specified directory if one doesn't exists
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0 )
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) #creates a TextureSampleParameter2D expression for base color and also sets its name and connects it to the BaseColor property

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) #creates a TextureSampleParameter2D expression for normal map, assigns a default material and connects it to the Normal property

        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallic)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC) #creates a TextureSampleParameter2D expression for occlusion, roughness, and metallic, sets the parameter name and connects each channel to the appropriate material property

        EditorAssetLibrary.save_asset(baseMat.get_path_name()) #saves the newly created material asset and returns it
        return baseMat
