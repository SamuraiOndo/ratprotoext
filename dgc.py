from binary_reader import BinaryReader
import sys
from pathlib import Path
import os
# stolen from emily (https://github.com/widberg/fmt_fuel/blob/master/inc_fuel.py#L18), thank you!
def decompress(data):
    WINDOW_LOG = 14
    WINDOW_SIZE = 1 << WINDOW_LOG
    WINDOW_MASK = (1 << WINDOW_LOG) - 1

    bs = BinaryReader(data)
    bs.set_endian(False)
    decompressedSize = bs.read_uint32()
    compressedSize = bs.read_uint32()
    windowBuffer = bytearray(WINDOW_SIZE)
    decompressed = BinaryReader()
    flagbit = 0
    pos = 0
    while decompressed.size() != decompressedSize:
        if flagbit <= 1:
            flagmask = bs.read_uint8() << 24
            flagmask |= bs.read_uint8() << 16
            flagmask |= bs.read_uint8() << 8
            flagmask |= bs.read_uint8()
            flagbit = 32 - 1
            lenbits = WINDOW_LOG - (flagmask & 3)

        flag = flagmask >> flagbit & 1
        flagbit -= 1
        currentByte = bs.read_uint8()

        if flag == 0:
            windowBuffer[pos & WINDOW_MASK] = currentByte
            pos += 1
            decompressed.write_uint8(currentByte)
        else:
            d = bs.read_uint8()
            j = (currentByte << 8) + d

            length = (j >> lenbits) + 3
            d = (j & (1 << lenbits) - 1) + 1

            for j in range(length):
                currentByte = windowBuffer[pos - d & WINDOW_MASK]
                windowBuffer[pos & WINDOW_MASK] = currentByte
                pos += 1
                decompressed.write_uint8(currentByte)
    return decompressed.buffer()

Mypath = Path(sys.argv[1])
directory = str(Mypath.resolve().parent)
Myfilename = Mypath.name
f = Mypath.open("rb")
output_path = directory / Path(Myfilename + ".unpack")
output_path.mkdir(parents=True, exist_ok=True)
reader = BinaryReader(f.read())
reader.set_endian(True)
reader.seek(256)
blockcount = reader.read_uint32()
reader.seek(24,1)
objectCountList = []
blockPaddedSizeList = []
blockSizeList = []
for i in range(64):
    objectCountList.append(reader.read_uint32())
    blockPaddedSizeList.append(reader.read_uint32())
    blockSizeList.append(reader.read_uint32())
    reader.read_bytes(12)
reader.read_bytes(228)
for i in range(blockcount):
    for j in range(objectCountList[i]):
        dataSize = reader.read_uint32()
        compressedSize = reader.read_uint32()
        classCrc32 = reader.read_uint32()
        nameCrc32 = reader.read_uint32()
        if (compressedSize != 0):
            readFile = reader.read_bytes(compressedSize)
            file = decompress(readFile)
        else:
            file = reader.read_bytes(dataSize)
        if (classCrc32 == 549480509):
            fileextension = "Omni_Z"
        elif (classCrc32 == 705810152):
            fileextension = "Rtc_Z"
        elif (classCrc32 == 838505646):
            fileextension = "GenWorld_Z"
        elif (classCrc32 == 848525546):
            fileextension = "LightData_Z"
        elif (classCrc32 == 849267944):
            fileextension = "Sound_Z"
        elif (classCrc32 == 849861735):
            fileextension = "MaterialObj_Z"
        elif (classCrc32 == 866453734):
            fileextension = "RotShape_Z"
        elif (classCrc32 == 954499543):
            fileextension = "ParticlesData_Z"
        elif (classCrc32 == 968261323):
            fileextension = "World_Z"
        elif (classCrc32 == 1114947943):
            fileextension = "Warp_Z"
        elif (classCrc32 == 1135194223):
            fileextension = "Spline_Z"
        elif (classCrc32 == 1175485833):
            fileextension = "Animation_Z"
        elif (classCrc32 == 1387343541):
            fileextension = "Mesh_Z"
        elif (classCrc32 == 1391959958):
            fileextension = "UserDefine_Z"
        elif (classCrc32 == 1396791303):
            fileextension = "Skin_Z"
        elif (classCrc32 == 1471281566):
            fileextension = "Bitmap_Z"
        elif (classCrc32 == 1536002910):
            fileextension = "Fonts_Z"
        elif (classCrc32 == 1625945536):
            fileextension = "RotShapeData_Z"
        elif (classCrc32 == 1706265229):
            fileextension = "Surface_Z"
        elif (classCrc32 == 1910554652):
            fileextension = "SplineGraph_Z"
        elif (classCrc32 == 705810152):
            fileextension = "Lod_Z"
        elif (classCrc32 == 2204276779):
            fileextension = "Material_Z"
        elif (classCrc32 == 2245010728):
            fileextension = "Node_Z"
        elif (classCrc32 == 2259852416):
            fileextension = "Binary_Z"
        elif (classCrc32 == 2398393906):
            fileextension = "CollisionVol_Z"
        elif (classCrc32 == 2906362741):
            fileextension = "WorldRef_Z"
        elif (classCrc32 == 3312018398):
            fileextension = "Particles_Z"
        elif (classCrc32 == 3412401859):
            fileextension = "LodData_Z"
        elif (classCrc32 == 3611002348):
            fileextension = "Skel_Z"
        elif (classCrc32 == 3626109572):
            fileextension = "MeshData_Z"
        elif (classCrc32 == 3747817665):
            fileextension = "SurfaceDatas_Z"
        elif (classCrc32 == 3834418854):
            fileextension = "MaterialAnim_Z"
        elif (classCrc32 == 3845834591):
            fileextension = "GwRoad_Z"
        elif (classCrc32 == 4096629181):
            fileextension = "GameObj_Z"
        elif (classCrc32 == 4240844041):
            fileextension = "Camera_Z"
        elif (classCrc32 == 4117606081):
            fileextension = "AnimFrame_Z"
        elif (classCrc32 == 3979333606):
            fileextension = "CameraZone_Z"
        elif (classCrc32 == 72309972):
            fileextension = "Occluder_Z"
        elif (classCrc32 == 1390918523):
            fileextension = "Graph_Z"
        elif (classCrc32 == 1918499807):
            fileextension = "Light_Z"
        elif (classCrc32 == 3210467954):
            fileextension = "HFogData_Z"
        elif (classCrc32 == 2735949084):
            fileextension = "HFog_Z"
        elif (classCrc32 == 2203168663):
            fileextension = "Flare_Z"
        elif (classCrc32 == 1393846573):
            fileextension = "FlareData_Z"
        else:
            fileextension = str(classCrc32)
        fileName = (str(nameCrc32) + "." + fileextension)
        print("Writing to " + fileName)
        output_file = output_path / (fileName)
        fe = open(output_file, "wb")
        fe.write(file)
        fe.close()
    padding = reader.read_bytes((blockPaddedSizeList[i]-blockSizeList[i]))
