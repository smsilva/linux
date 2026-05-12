# ODP Progressive Reveal Animations

## Reference file

`assets/animation-example.odp` — working example of progressive reveal in LibreOffice/Impress.

## How progressive reveal works in ODP

LibreOffice hides items with entrance animations until triggered by a click. No manual `display:none` needed — the animation engine controls visibility.

## XML pattern

This goes inside `<presentation:show-shape>` → `<draw:frame>` → the slide's `<presentation:animation-group>` in `content.xml`:

```xml
<anim:par presentation:node-type="timing-root">
  <anim:seq presentation:node-type="main-sequence">
    <anim:par smil:begin="next">
      <anim:par smil:begin="0s">
        <anim:par smil:begin="0s" smil:fill="hold"
                  presentation:node-type="on-click"
                  presentation:preset-class="entrance"
                  presentation:preset-id="ooo-entrance-appear">
          <anim:set smil:begin="0s" smil:dur="0.001s" smil:fill="hold"
                    smil:targetElement="ITEM_ID" anim:sub-item="text"
                    smil:attributeName="visibility" smil:to="visible"/>
        </anim:par>
      </anim:par>
    </anim:par>
    <!-- repeat <anim:par smil:begin="next"> block for each item -->
  </anim:seq>
</anim:par>
```

Each `<anim:par smil:begin="next">` block = one click. Repeat for every item, each with its own `ITEM_ID`.

## Marking list items

Each `<text:p>` element that should be animated needs matching IDs:

```xml
<text:p xml:id="item1" text:id="item1">First bullet</text:p>
<text:p xml:id="item2" text:id="item2">Second bullet</text:p>
```

The `smil:targetElement` in the animation block must match the `xml:id` exactly.

## Dimming previous items (contrast principle)

To implement Principle 4 (contrast guides attention), previous items should appear dimmed. In ODP this is achieved with a second animation that changes the text color of the previous item when the next one appears:

```xml
<!-- When item 2 appears, dim item 1 -->
<anim:par smil:begin="next">
  <anim:par smil:begin="0s">
    <!-- Make item 2 visible -->
    <anim:par smil:begin="0s" smil:fill="hold"
              presentation:node-type="on-click"
              presentation:preset-class="entrance"
              presentation:preset-id="ooo-entrance-appear">
      <anim:set smil:begin="0s" smil:dur="0.001s" smil:fill="hold"
                smil:targetElement="item2" anim:sub-item="text"
                smil:attributeName="visibility" smil:to="visible"/>
    </anim:par>
    <!-- Dim item 1 -->
    <anim:animate smil:begin="0s" smil:dur="0.001s" smil:fill="hold"
                  smil:targetElement="item1" anim:sub-item="text"
                  smil:attributeName="color" smil:to="#565E6B"/>
  </anim:par>
</anim:par>
```

## Editing ODP XML

ODP files are ZIP archives. To edit manually:

```bash
# Unpack
unzip presentation.odp -d presentation-unpacked/

# Edit content.xml
# ...

# Repack (from inside the directory)
cd presentation-unpacked/
zip -r ../presentation.odp .
```
