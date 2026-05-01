import numpy as np
import slicer
import os

data = np.fromfile(
    r"/path/to/XCAT_results/pht4_act_1.bin",
    dtype=np.float32
)

data = data.reshape((44, 512, 512))

node = slicer.util.addVolumeFromArray(data)
node.SetName("XCAT_atn")
node.SetSpacing([1.172, 1.172, 3.0])

slicer.util.setSliceViewerLayers(background=node)
slicer.util.resetSliceViews()

volumeNode = slicer.util.getNode("XCAT_atn")
slicer.util.exportNode(volumeNode, r"/path/to/output/XCAT_atn.nrrd")

outputDir = r"/path/to/output/DICOM_output"
os.makedirs(outputDir, exist_ok=True)

parameters = {
    "inputVolume": slicer.util.getNode("XCAT_atn"),
    "dicomDirectory": outputDir
}

slicer.cli.runSync(slicer.modules.createdicomseries, None, parameters)
