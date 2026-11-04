---
description: Sources, licences, and changes for schemas used by the illustrative Write binding.
---

# Example schema attribution

The [Write examples](README.md#non-normative-write-examples) use selected
[PublicSchema](https://publicschema.org/) models and their GeoJSON dependency.
These models are illustrative domain choices. They are not requirements of the
Write operations in the shared Registry API contract.

## PublicSchema

The reference schemas and context come from
[PublicSchema](https://github.com/PublicSchema/publicschema.org), revision
`7352b360706c4002033e6db2919d9d3b6d13e7a8`, as published on 5 October 2026.
They are licensed under
[Creative Commons Attribution 4.0 International](../../api/examples/publicschema/LICENSE-CC-BY-4.0.txt).
The repository retains the unmodified source files and their provenance record.

The example OpenAPI uses an offline mirror. That mirror removes each canonical
`$id` and rewrites PublicSchema and GeoJSON `$ref` values to local files.
It preserves the other schema keywords and values. These changes allow local
reference resolution without selecting a different domain model.

## GeoJSON Geometry

The Geometry schema comes from the
[GeoJSON schema project](https://github.com/geojson/schema), published revision
`f2bc6e8f1e8e1ba376d901914ecf8d0fed947d6e`. The unmodified source is retained
in the repository; its offline mirror applies the same identifier transformations
described above. The following MIT notice applies to this dependency.

Copyright (c) 2018 Tim Schaub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
