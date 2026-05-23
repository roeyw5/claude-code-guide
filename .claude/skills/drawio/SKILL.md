---
name: drawio
description: Generate draw.io diagrams as native .drawio XML files for viewing/editing in the VS Code drawio extension or app.diagrams.net
allowed-tools: Bash, Write
---

# Draw.io Diagram Skill

Generate draw.io diagrams as native `.drawio` XML files. The user opens them in the VS Code drawio extension (already installed) or at `app.diagrams.net` — no CLI export, no rasterizing.

If the user explicitly asks for a PNG/SVG/PDF, tell them to right-click the `.drawio` tab in VS Code and use "Export" — it's one click and works without the headless-export hassle.

## How to create a diagram

1. **Generate draw.io XML** in mxGraphModel format for the requested diagram
2. **Write the XML** to a `.drawio` file in the current working directory using the Write tool
3. **Validate the XML** — run `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.drawio'); print('Valid')"` and fix any errors before reporting done
4. **Tell the user the file path.** Don't try to `xdg-open` it — VS Code picks it up when the user clicks the file.

## Page size guidance

Set `pageWidth` and `pageHeight` on the `<mxGraphModel>` element to fit your content. Common presets:

| Size | pageWidth | pageHeight | Good for |
| ---- | --------- | ---------- | -------- |
| Small (A4 landscape) | 1169 | 827 | Simple flowcharts, small diagrams |
| Medium (A3 landscape) | 1587 | 1123 | Moderate architecture diagrams |
| Large | 2800 | 1600 | Detailed multi-section diagrams |
| Extra large | 3600 | 2400 | Full infrastructure with many groups |

Estimate your total content area first, then pick the next size up. Add ~20% margin beyond your content bounds.

## File naming

- Use a descriptive filename based on the diagram content (e.g., `login-flow.drawio`, `database-schema.drawio`)
- Use lowercase with hyphens for multi-word names
- Always use the `.drawio` extension

## XML format

A `.drawio` file is native mxGraphModel XML. Always generate XML directly — Mermaid and CSV formats require server-side conversion and cannot be saved as native files.

### Basic structure

Every `.drawio` file must wrap `mxGraphModel` in `mxfile > diagram`. The bare `<mxGraphModel>` form opens in some versions of the desktop app but fails to import in the web app (`app.diagrams.net`) and breaks the CLI's `--embed-diagram` round-trip. Always emit the full wrapper:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="main" name="Page-1">
    <mxGraphModel pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="2" value="Example" style="rounded=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- Cell `id="0"` is the root layer
- Cell `id="1"` is the default parent layer
- All diagram elements use `parent="1"` unless using containers/swimlanes
- The `diagram` element's `id` and `name` show up as page metadata; pick descriptive values

### Containers and swimlanes

Use `swimlane` style to create grouping containers (regions, environments, service categories). Key points:

- Child cells use `parent="<container_id>"` and their x/y coordinates are **relative to the container**
- Add `collapsible=0;` to prevent the container from being collapsible in the editor
- `startSize=36` controls the header height where the title is displayed
- Containers can be nested (e.g., a service group inside a region)

```xml
<mxCell id="region" value="Region Name" style="swimlane;startSize=36;fillColor=#f0f4ff;strokeColor=#1976d2;collapsible=0;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="800" height="600" as="geometry"/>
</mxCell>
<mxCell id="child" value="Service" style="rounded=1;" vertex="1" parent="region">
  <mxGeometry x="20" y="50" width="120" height="60" as="geometry"/>
</mxCell>
```

### Edges across containers

When connecting cells that live in **different containers**, the edge must use `parent="1"` (the root layer), not the parent of either endpoint. This is the most common source of broken connections.

```xml
<mxCell id="cross_edge" value="label" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="cellInContainerA" target="cellInContainerB" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

Edges between cells in the **same** container can use that container as parent.

### Common styles

**Rounded rectangle:**

```xml
<mxCell id="2" value="Label" style="rounded=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

**Diamond (decision):**

```xml
<mxCell id="3" value="Condition?" style="rhombus;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="120" height="80" as="geometry"/>
</mxCell>
```

**Arrow (edge):**

```xml
<mxCell id="4" value="" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**Labeled arrow:**

```xml
<mxCell id="5" value="Yes" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="3" target="6" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### Useful style properties

| Property                           | Values        | Use for                |
| ---------------------------------- | ------------- | ---------------------- |
| `rounded=1`                        | 0 or 1        | Rounded corners        |
| `whiteSpace=wrap`                  | wrap          | Text wrapping          |
| `fillColor=#dae8fc`                | Hex color     | Background color       |
| `strokeColor=#6c8ebf`              | Hex color     | Border color           |
| `fontColor=#333333`                | Hex color     | Text color             |
| `shape=cylinder3`                  | shape name    | Database cylinders     |
| `shape=mxgraph.flowchart.document` | shape name    | Document shapes        |
| `ellipse`                          | style keyword | Circles/ovals          |
| `rhombus`                          | style keyword | Diamonds               |
| `edgeStyle=orthogonalEdgeStyle`    | style keyword | Right-angle connectors |
| `edgeStyle=elbowEdgeStyle`         | style keyword | Elbow connectors       |
| `dashed=1`                         | 0 or 1        | Dashed lines           |
| `swimlane`                         | style keyword | Swimlane containers    |

## AWS icons

draw.io ships the AWS icon set built in — no install, plugin, or external stencil files needed. Identical rendering in desktop and web. Use the current set (`mxgraph.aws4.*`, "AWS 2019/Architecture Icons"); avoid the older `aws2`/`aws3`/AWS17 sets.

There are three things you'll emit: **resource icons** (most services), **plain shapes** (a few exceptions like ALB, VPC endpoint), and **group containers** (Cloud / Region / VPC / AZ / Subnet).

### Resource icon (colored square + white glyph)

This is the default for almost every service. Replace `<SERVICE>`, `<DARK>`, `<LIGHT>`:

```
sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=<LIGHT>;gradientDirection=north;fillColor=<DARK>;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<SERVICE>;
```

Standard size is 78×78 px. Mandatory: `strokeColor=#ffffff`, `gradientDirection=north`, `aspect=fixed` — drop any of these and the icon disappears or distorts.

| Service | resIcon token | fillColor (dark) | gradientColor (light) |
|---|---|---|---|
| EC2 | `ec2` | `#D05C17` | `#F78E04` |
| Lambda | `lambda` | `#D05C17` | `#F78E04` |
| S3 | `s3` | `#277116` | `#60A337` |
| RDS | `rds` | `#3334B9` | `#4D72F3` |
| CloudFront | `cloudfront` | `#8C4FFF` | `#E7157B` |
| Route 53 | `route_53` | `#5A30B5` | `#945DF2` |
| API Gateway | `api_gateway` | `#BC1356` | `#FF4F8B` |
| SQS | `sqs` | `#BC1356` | `#FF4F8B` |
| SNS | `sns` | `#BC1356` | `#FF4F8B` |
| CloudWatch | `cloudwatch` | `#BC1356` | `#FF4F8B` |
| IAM | `iam` | `#BC1356` | `#FF4F8B` |
| ACM | `certificate_manager_3` | `#C7131F` | `#F54749` |

For service tokens not in the table, search the [aws4 stencil reference](https://github.com/Hands-On-Vibe-Coding/ecs-fargate-fast-scaleout/blob/main/docs/aws-2025-icons-drawio.md) or open the AWS shape panel in the GUI and use "Edit Style" on the icon to read its `resIcon=` value.

### Plain shape (no gradient square)

A handful of AWS shapes don't use the resourceIcon wrapper — ALB, VPC endpoint, IAM policy doc, illustration icons. Pattern:

```
sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#4D27AA;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.<SHAPE>;
```

Useful tokens: `application_load_balancer`, `endpoints`, `policy`, `illustration_users`.

### Group containers (Cloud / Region / VPC / AZ / Subnet)

These are the dashed/solid-bordered regions that wrap resources. Single template, swap `grIcon` + `strokeColor`. Children placed inside use coordinates **relative to the container**.

```
points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.<GR>;strokeColor=<COLOR>;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;
```

| Container | grIcon token | strokeColor | Notes |
|---|---|---|---|
| AWS Cloud | `group_aws_cloud_alt` | `#232F3E` | Outermost wrapper |
| Region | `group_region` | `#00A4A6` | Add `dashed=1;` |
| VPC | `group_vpc` | `#248814` | Solid |
| Availability Zone | `group_az` | `#147EBA` | Add `dashed=1;` |
| Public Subnet | `group_security_group` | `#7AA116` | Solid |
| Private Subnet | `group_security_group` | `#147EBA` | Solid |
| Corporate DC | `group_corporate_data_center` | `#7D8998` | For on-prem |

### Edges between AWS shapes

Use simple edges — no orthogonal routing by default (AWS reference diagrams use straight or simple lines):

```xml
<mxCell id="e1" style="edgeStyle=none;html=1;" edge="1" parent="1" source="ec2" target="rds">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

Add `dashed=1;` for async/event-driven edges (e.g., Lambda → SNS, SQS triggers).

Remember: edges that cross containers must use `parent="1"`, not the container's id. See "Edges across containers" above.

## CRITICAL: XML well-formedness

- **Do NOT use XML comments at all.** Comments with `--` cause parse errors (`--` is illegal inside `<!-- -->`), and draw.io ignores comments anyway. If you need to organize sections, use whitespace and descriptive `id` values instead.
- Escape special characters in attribute values: `&amp;`, `&lt;`, `&gt;`, `&quot;`
- Always use unique `id` values for each `mxCell`
- **Always validate after writing.** Run: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.drawio'); print('Valid')"` before opening the file.
