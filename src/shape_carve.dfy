method ShapeCarve(dims: seq<nat>, views: seq<seq<int>>, mask_color: int, skip: seq<bool>)
  /* returns (res: tuple<array<int>, array<int>>) */
  requires |dims| == 3
  requires dims[0] > 1
  requires dims[1] > 1
  requires dims[2] > 1
  requires |views| == 13  // depth.Length + 1
  requires |skip| == 7
  requires |views[6]| >= dims[0] * dims[1] && |views[6]| >= dims[1] * dims[2] && |views[6]| >= dims[2] * dims[0]
{
    var x: array<int> := new int[3];
    var volumeSize: int := dims[0] * dims[1] * dims[2];
    var volume: array<int> := new int[volumeSize];
    var depth: array<array<int>> := new array<int>[12]; // was 6, but needs append space
    var depthLength: int := 6;
    var oldDepthLength: int := 6;
    
    for i := 0 to volumeSize { volume[i] := -1; }
    
    var d: int, u: int, v: int, s: int, s_op: int, valsSize: int, viewIndex: int, buf_idx: int, vol_idx: int, color: int, a: int, b: int, c: int, idx: int, t: int, fnum: int, fcolor: int, fdepth: int;

    for d := 0 to 3
    invariant depthLength == 6 + d * 2
    {
        u := (d + 1) % 3;
        v := (d + 2) % 3;
        s := 0;
        var i := 0;
        while s <= dims[d] - 1
        /* for i := 0 to 2 */
        invariant i * (dims[d] - 1) == s
        invariant 0 <= s <= 2 * (dims[d] - 1)
        invariant depthLength == 6 + d * 2 + i
        {
            valsSize := dims[u] * dims[v];
            var vals: array<int> := new int[valsSize];
            viewIndex := oldDepthLength; // length of depth array
            var view: seq<int> := views[viewIndex];
            s_op := if s == 0 then dims[d] - 1 else 0;
            for i := 0 to valsSize {
                vals[i] := if !skip[viewIndex] && view[i] == mask_color then s_op else s;
            }
            depth[depthLength] := vals;
            depthLength := depthLength + 1;
            s := s + dims[d] - 1;
            i := i + 1;
        }
        assert i == 2;
        /* for xv := 0 to dims[v] { */
        /*     for xu := 0 to dims[u] { */
        /*         for xd := depth[2 * d + 1][xu + xv * dims[u]] to depth[2 * d][xu + xv * dims[u]] + 1 { */
        /*             var x0 := if d == 0 then xd else if u == 0 then xu else xv; */
        /*             var x1 := if d == 1 then xd else if u == 1 then xu else xv; */
        /*             var x2 := if d == 2 then xd else if u == 2 then xu else xv; */
        /*             volume[x0 + dims[0] * (x1 + dims[1] * x2)] := mask_color; */
        /*         } */
        /*     } */
        /* } */
    }

    var removed: int := 1;

    while removed > 0 {
        removed := 0;
        for d := 0 to 3 {
/*             u := (d + 1) % 3; */
/*             v := (d + 2) % 3; */
/*             for s := -1; s <= 1; s := s + 2 { */
/*                 var v_num: int := 2 * d + (if s < 0 then 1 else 0); */
/*                 if skip[v_num] { continue; } */
/*                 var aview: array<int> := views[v_num]; */
/*                 var adepth: array<int> := depth[v_num]; */
/*                 for x[v] := 0; x[v] < dims[v]; x[v] := x[v] + 1 */
/*                 for x[u] := 0; x[u] < dims[u]; x[u] := x[u] + 1 { */
/*                     buf_idx := x[u] + x[v] * dims[u]; */
/*                     for x[d] := adepth[buf_idx]; 0 <= x[d] && x[d] < dims[d]; x[d] := x[d] + s { */
/*                         vol_idx := x[0] + dims[0] * (x[1] + dims[1] * x[2]); */
/*                         color := volume[vol_idx]; */
/*                         if color == mask_color { continue; } */
/*                         color := volume[vol_idx] := aview[x[u] + dims[u] * x[v]]; */
/*                         var consistent: bool := true; */
/*                         for a := 0; consistent && a < 3; a := a + 1 { */
/*                             b := (a + 1) % 3; */
/*                             c := (a + 2) % 3; */
/*                             idx := x[b] + dims[b] * x[c]; */
/*                             for t := 0; t < 2; t := t + 1 { */
/*                                 fnum := 2 * a + t; */
/*                                 if skip[fnum] { continue; } */
/*                                 fcolor := views[fnum][idx]; */
/*                                 fdepth := depth[fnum][idx]; */
/*                                 if (t != 0 ? fdepth <= x[a] : x[a] <= fdepth) && fcolor != color { */
/*                                     consistent := false; */
/*                                     break; */
/*                                 } */
/*                             } */
/*                         } */
/*                         if consistent { break; } */
/*                         removed := removed + 1; */
/*                         volume[vol_idx] := mask_color; */
/*                     } */
/*                     adepth[buf_idx] := x[d]; */
/*                 } */
            }
        }
    }

method fillMissingColors(x: array<int>, dims: seq<nat>, volume: array<int>)
modifies volume
requires |dims| == 3
requires volume.Length == dims[0] * dims[1] * dims[2]
{
    var n: int := 0;
    for i := 0 to dims[2] {
        for j := 0 to dims[1] {
            for k := 0 to dims[0] {
                if volume[k] < 0 {
                    volume[k] := 0xff00ff;
                }
                n := n + 1;
            }
        }
    }
}

