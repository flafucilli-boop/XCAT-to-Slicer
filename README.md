# XCAT Binary to DICOM / STL using 3D Slicer

Pipeline for converting XCAT binary phantom outputs (`.bin`) into:

- DICOM series
- NRRD volumes
- STL meshes for 3D printing

using Python inside 3D Slicer.

---

# Requirements

Software required:

- 3D Slicer
- NumPy
- XCAT binary output files (`_act_1.bin` or `_atn_1.bin`)

Recommended software for mesh cleanup:

- Rhino
- MeshMixer

---

# Important Note

> Replace all placeholder paths (e.g. `/path/to/...`) with the correct paths on your local machine.

---

# Repository Structure

```text
XCAT-to-Slicer/
│
├── README.md
├── scripts/
│   ├── xcat_bin_to_dicom.py
│   └── xcat_bin_to_stl.py
│
├── images/
│   ├── slicer_volume.png
│   ├── segmentation.png
│   └── stl_export.png
│
└── examples/
    └── sample_log_file.log
```

---

# XCAT Binary → DICOM

## 1. Load Binary Volume

Open:

```text
View → Python Interactor
```

Paste the following code:

```python
import numpy as np
import slicer

# Path to the XCAT binary file
binaryFile = r"/path/to/XCAT_results/pht4_act_1.bin"

# Load binary data
data = np.fromfile(
    binaryFile,
    dtype=np.float32
)

# Reshape volume
data = data.reshape((44, 512, 512))

# Create Slicer volume node
node = slicer.util.addVolumeFromArray(data)

# Set node name
node.SetName("XCAT_atn")

# Set voxel spacing (mm)
node.SetSpacing([1.172, 1.172, 3.0])

# Display volume
slicer.util.setSliceViewerLayers(background=node)
```

---

## 2. Center Slice Views

```python
slicer.util.resetSliceViews()
```

---

## 3. Export as NRRD

```python
# Output NRRD file
outputNRRD = r"/path/to/output/XCAT_atn.nrrd"

# Get volume node
volumeNode = slicer.util.getNode("XCAT_atn")

# Export NRRD
slicer.util.exportNode(
    volumeNode,
    outputNRRD
)
```

The `.nrrd` file will be saved in the selected output folder.

---

## 4. Convert to DICOM

```python
import os

# Output DICOM directory
outputDir = r"/path/to/output/DICOM_output"

# Create directory if it does not exist
os.makedirs(outputDir, exist_ok=True)

# Conversion parameters
parameters = {
    "inputVolume": slicer.util.getNode("XCAT_atn"),
    "dicomDirectory": outputDir
}

# Run DICOM conversion
slicer.cli.runSync(
    slicer.modules.createdicomseries,
    None,
    parameters
)
```

The generated `.dcm` files will appear inside:

```text
DICOM_output
```

---

# Volume Parameters

Parameters extracted from the `.log` file:

| Parameter | Value |
|---|---|
| nx, ny | 512 × 512 |
| nz | 44 |
| slice range | 278–321 |
| pixel size | 1.172 mm |
| slice thickness | 3.0 mm |
| data type | float32 |

---

# XCAT Binary → STL

## 1. Load Activity Volume

Open:

```text
View → Python Interactor
```

Paste:

```python
import numpy as np
import slicer

# Path to the activity binary file
binaryFile = r"/path/to/XCAT_results/pht2.2_act_1.bin"

# Load binary data
data = np.fromfile(
    binaryFile,
    dtype=np.float32
)

# Reshape volume
data = data.reshape((44, 512, 512))

# Create Slicer volume node
node = slicer.util.addVolumeFromArray(data)

# Set node name
node.SetName("XCAT_act")

# Set voxel spacing (mm)
node.SetSpacing([1.172, 1.172, 3.0])

# Display volume
slicer.util.setSliceViewerLayers(background=node)

# Center slice views
slicer.util.resetSliceViews()
```

---

## 2. Segment the Organ

### Open Segment Editor

```text
Modules → Segment Editor
```

### Create a Segment

1. Click `Add`
2. Select `Threshold`
3. Set threshold values
4. Click `Apply`
5. Enable `Show 3D`

---

## Example Thresholds

| Organ | Threshold |
|---|---|
| Prostate | 25–35 |
| Liver | ~75 |
| Kidneys | ~75 |
| Heart | ~75 |

Thresholds may vary depending on the simulation.

---

## 3. Export STL

Open:

```text
Modules → Segmentations
```

Scroll to:

```text
Export/Import
```

Set:

- Destination folder
- File format = STL
- Reference volume = `XCAT_act`

Then click:

```text
Export
```

The STL mesh will be generated in the selected folder.

---

# Important Notes

## Use the Correct Binary File

For segmentation and STL generation:

```text
Use *_act_1.bin
```

Do NOT use:

```text
*_atn_1.bin
```

for organ extraction.

---

# Mesh Cleanup

Generated STL meshes may require post-processing before 3D printing.

Recommended software:

- Rhino
- MeshMixer

Typical operations:

- hole filling
- smoothing
- mesh repair
- decimation

---

# Troubleshooting

## Wrong Volume Shape

If Slicer shows distorted geometry:

- verify `reshape()`
- verify voxel spacing
- verify slice number (`nz`)

Example:

```python
data = data.reshape((44, 512, 512))
```

---

## Empty Segmentation

Possible causes:

- incorrect threshold
- wrong binary file
- wrong intensity scaling

Try adjusting threshold values.

---

# References

- XCAT Phantom
- 3D Slicer Documentation
- NumPy Documentation

---

# License

This repository is intended for educational and research purposes.
