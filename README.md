A collection of dataloaders for common dataset.

Prepare data according to the instructions written in `README.md` and `download.sh` in each directory. See `demo.ipynb` to understand how to use them. 

## 1. COCO

## 2. IAM Handwriting

### example
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<WhiteboardCaptureSession> <!-- root -->
  <WhiteboardDescription>
    <SensorLocation corner="top_left"/>
    <DiagonallyOppositeCoords x="6512" y="1376"/>   <!-- x_offset, root[0][1].attrib['x'] -->
    <VerticallyOppositeCoords x="966" y="1376"/>
    <HorizontallyOppositeCoords x="6512" y="787"/>
  </WhiteboardDescription>
  <StrokeSet>
    <Stroke colour="black" start_time="769.05" end_time="769.64">  <!-- for stroke in root[1].findall('Stroke') -->
      <Point x="1073" y="1058" time="769.05"/> <!-- for point in stroke.findall('Point')  -->
      <Point x="1072" y="1085" time="769.07"/> <!-- point.attrib['x'] = 1073, point.attrib['y'] = 1085 -->
      ...
      <Point x="1204" y="1330" time="769.64"/>
    </Stroke>
    <Stroke colour="black" start_time="769.70" end_time="769.90">
      <Point x="1176" y="1237" time="769.70"/>
      ...
      <Point x="1014" y="1243" time="769.90"/>
    </Stroke>
    ...
  </StrokeSet>
</WhiteboardCaptureSession>

```
