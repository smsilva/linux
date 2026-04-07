# draw.io XML Reference

Source: https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/xml-reference.md

## Core Structure

Every diagram must have this exact structure:

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- all diagram cells with parent="1" -->
  </root>
</mxGraphModel>
```

- `id="0"` — root layer (required)
- `id="1"` — default parent layer (required, parent="0")
- All diagram elements use `parent="1"` unless using multiple layers
- `adaptiveColors="auto"` — enables dark mode color inversion

## Shape Syntax

```xml
<mxCell id="unique-id" value="Label" style="rounded=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

## Edge Syntax (CRITICAL)

Every edge cell MUST include an expanded `<mxGeometry>` child — self-closing edge cells fail to render:

```xml
<mxCell id="e1" edge="1" parent="1" source="cellA" target="cellB" style="edgeStyle=orthogonalEdgeStyle;html=1;">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Key Style Properties

| Property | Values | Purpose |
|----------|--------|---------|
| `rounded` | `0`, `1` | Rounded corners |
| `whiteSpace` | `wrap` | Word wrap in labels |
| `html` | `1` | Enable HTML in labels |
| `fillColor` | `#HEX` | Background color |
| `strokeColor` | `#HEX` | Border color |
| `fontColor` | `#HEX` | Text color |
| `fontStyle` | `1`=bold, `2`=italic, `4`=underline | Text style |
| `fontSize` | integer | Font size in px |
| `align` | `left`, `center`, `right` | Horizontal text alignment |
| `verticalAlign` | `top`, `middle`, `bottom` | Vertical text alignment |
| `spacingLeft` | integer | Left padding for text |
| `shape` | see below | Shape type |
| `container` | `1` | Enable as container |
| `swimlane` | (in style string) | Titled container with header |
| `startSize` | integer | Header height for swimlanes |
| `dashed` | `0`, `1` | Dashed border/edge |
| `strokeWidth` | integer | Border/edge thickness |

## Common Shape Values

| Style | Shape |
|-------|-------|
| `shape=cloud` | Cloud |
| `shape=cylinder3` | Database/cylinder |
| `rhombus` | Diamond / decision |
| `ellipse` | Circle/oval |
| `shape=mxgraph.aws4.application_load_balancer` | AWS ALB icon |
| `shape=mxgraph.aws4.eks` | AWS EKS icon |

## Edge Styles

| Style | Description |
|-------|-------------|
| `edgeStyle=orthogonalEdgeStyle` | Right-angle connectors (recommended) |
| `edgeStyle=elbowEdgeStyle` | Elbow connector |
| `edgeStyle=entityRelationEdgeStyle` | ER diagram style |
| `dashed=1` | Dashed line |
| `endArrow=none` | No arrowhead at end |
| `endArrow=open;endFill=0` | Open arrowhead (not filled) |
| `startArrow=...` | Arrowhead at start |
| `strokeWidth=2` | Thicker line |

## Connection Point Control (edges)

```
exitX=0.5;exitY=1;exitDx=0;exitDy=0    → exit from bottom center
entryX=0.5;entryY=0;entryDx=0;entryDy=0 → enter from top center
```

## Containment (parent-child)

Children use coordinates relative to the container's content area (after the header for swimlanes):

```xml
<mxCell id="container" value="Title" style="swimlane;startSize=25;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="400" height="300" as="geometry"/>
</mxCell>

<mxCell id="child" value="Child" style="rounded=1;" vertex="1" parent="container">
  <mxGeometry x="20" y="30" width="120" height="60" as="geometry"/>
</mxCell>
```

- Edges between cells in different containers: use `parent="1"` for the edge
- Minimum spacing: 60px between nodes; 20px+ straight segment before arrowheads

## Layers

Additional layers are `mxCell` elements with `parent="0"`:

```xml
<mxCell id="layer2" value="Layer Name" parent="0"/>
<mxCell id="cell1" parent="layer2" vertex="1">...</mxCell>
```

## Tags (visibility filters)

Use `<object>` wrapper with space-separated `tags` attribute:

```xml
<object label="My Shape" tags="aws production" id="s1">
  <mxCell style="rounded=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
  </mxCell>
</object>
```

## Metadata / Placeholders

```xml
<object label="%name% (%status%)" name="API Server" status="healthy" placeholders="1" id="s2">
  <mxCell style="rounded=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
  </mxCell>
</object>
```

## Dark Mode Colors

- `adaptiveColors="auto"` on mxGraphModel handles automatic color inversion
- For manual control: `fillColor=light-dark(#ffffff,#1e1e1e)`

## XML Well-formedness Rules (CRITICAL)

- **NEVER include XML comments** (`<!-- -->`) — strictly forbidden, causes parse errors
- Escape special characters in attribute values:
  - `&` → `&amp;`
  - `<` → `&lt;`
  - `>` → `&gt;`
  - `"` → `&quot;`
- All `id` values must be unique across the entire diagram
- `mxGeometry` must be a child element of `mxCell`, never inline
- Edge cells must NEVER be self-closing — always include `<mxGeometry relative="1" as="geometry"/>`

## Design Principles

- Use semantically appropriate shapes (cylinders for databases, diamonds for decisions, clouds for internet)
- For standard diagrams (flowcharts, UML, ERD): use basic geometric shapes
- For domain-specific diagrams (AWS, Kubernetes, network): use shape library icons when available
- Space nodes generously: 200px horizontal / 120px vertical minimum preferred
- Use orthogonal edge style with explicit waypoints when edges would overlap
- Localize labels to match the user's language
