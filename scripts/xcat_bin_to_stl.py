import numpy as np
import slicer

# ============================================================
# Load XCAT binary volume
# ============================================================

data = np.fromfile(
    r"/path/to/XCAT_results/pht2.2_act_1.bin",
    dtype=np.float32
)

data = data.reshape((44, 512, 512))

node = slicer.util.addVolumeFromArray(data)
node.SetName("XCAT_act")
node.SetSpacing([1.172, 1.172, 3.0])

slicer.util.setSliceViewerLayers(background=node)
slicer.util.resetSliceViews()
