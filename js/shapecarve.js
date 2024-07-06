"use strict";

function ShapeCarve(dims, views, mask_color, skip) {
  let x = new Int32Array(3)
    , volume = new Int32Array(dims[0] * dims[1] * dims[2])
    , depth = [];

  //Initialize volume
  for(let i=0; i<volume.length; ++i) {
    volume[i] = -1;
  }

  //Initialize depth fields
  for(let d=0; d<3; ++d) {
    let u = (d+1)%3
      , v = (d+2)%3;
    for(let s=0; s<=dims[d]-1; s+=dims[d]-1) {
      let vals = new Int32Array(dims[u] * dims[v])
        , view = views[depth.length]
        , s_op = (s === 0) ? dims[d]-1 : 0;
      for(let i=0; i<vals.length; ++i) {
        vals[i] = (!skip[depth.length] && view[i] === mask_color) ? s_op : s;
      }
      depth.push(vals);
    }

    //Clear out volume
    for(x[v]=0; x[v]<dims[v]; ++x[v])
    for(x[u]=0; x[u]<dims[u]; ++x[u])
    for(x[d]=depth[2*d+1][x[u]+x[v]*dims[u]]; x[d]<=depth[2*d][x[u]+x[v]*dims[u]]; ++x[d]) {
      volume[x[0]+dims[0]*(x[1] + dims[1]*x[2])] = mask_color;
    }
  }

  //Perform iterative seam carving until convergence
  let removed = 1;
  while(removed > 0) {
    removed = 0;
    for(let d=0; d<3; ++d) {
      let u = (d+1)%3
        , v = (d+2)%3;

      //Do front/back sweep
      for(let s=-1; s<=1; s+=2) {
        let v_num = 2*d + ((s<0) ? 1 : 0);
        if(skip[v_num]) {
          continue;
        }

        let aview = views[v_num]
          , adepth = depth[v_num];

        for(x[v]=0; x[v]<dims[v]; ++x[v])
        for(x[u]=0; x[u]<dims[u]; ++x[u]) {

          //March along ray
          let buf_idx = x[u] + x[v]*dims[u];
          for(x[d] = adepth[buf_idx]; 0<=x[d] && x[d]<dims[d]; x[d]+=s) {

            //Read volume color
            let vol_idx = x[0] + dims[0] * (x[1] + dims[1] * x[2])
              , color = volume[vol_idx];
            if(color === mask_color) {
              continue;
            }

            color = volume[vol_idx] = aview[x[u] + dims[u] * x[v]];

            //Check photoconsistency of volume at x
            let consistent = true;
            for(let a=0; consistent && a<3; ++a) {
              let b = (a+1)%3
                , c = (a+2)%3
                , idx = x[b] + dims[b] * x[c];
              for(let t=0; t<2; ++t) {
                let fnum = 2*a+t;
                if(skip[fnum]) {
                  continue;
                }
                let fcolor = views[fnum][idx]
                  , fdepth = depth[fnum][idx];
                if(t ?  fdepth <= x[a] : x[a] <= fdepth) {
                  if(fcolor !== color) {
                    consistent = false;
                    break;
                  }
                }
              }
            }
            if(consistent) {
              break;
            }

            //Clear out voxel
            ++removed;
            volume[vol_idx] = mask_color;
          }

          //Update depth value
          adepth[buf_idx] = x[d];
        }
      }
    }
  }


  //Do a final pass to fill in any missing colors
  let n = 0;
  for(x[2]=0; x[2]<dims[2]; ++x[2])
  for(x[1]=0; x[1]<dims[1]; ++x[1])
  for(x[0]=0; x[0]<dims[0]; ++x[0], ++n) {
    if(volume[n] < 0) {
      volume[n] = 0xff00ff;
    }
  }

  return { volume:volume, dims:dims };
}

