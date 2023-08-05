def ShapeCarve(dims, views, mask_color, skip):
    x = [0] * 3
    volume = [-1] * (dims[0] * dims[1] * dims[2])
    depth = []

    # Initialize volume
    for i in range(len(volume)):
        volume[i] = -1

    # Initialize depth fields
    for d in range(3):
        u = (d+1)%3
        v = (d+2)%3
        for s in range(0, dims[d], max(1, dims[d] - 1)):
            vals = [0] * (dims[u] * dims[v])
            view = views[len(depth)]
            s_op = dims[d]-1 if s == 0 else 0
            for i in range(len(vals)):
                vals[i] = s_op if not skip[len(depth)] and view[i] == mask_color else s
            depth.append(vals)

        # Clear out volume
        for x[v] in range(dims[v]):
            for x[u] in range(dims[u]):
                for x[d] in range(depth[2*d+1][x[u]+x[v]*dims[u]], depth[2*d][x[u]+x[v]*dims[u]] + 1):
                    volume[x[0]+dims[0]*(x[1] + dims[1]*x[2])] = mask_color

    # Perform iterative seam carving until convergence
    removed = 1
    while removed > 0:
        removed = 0
        for d in range(3):
            u = (d+1)%3
            v = (d+2)%3

            # Do front/back sweep
            for s in range(-1, 2, 2):
                v_num = 2*d + (1 if s<0 else 0)
                if skip[v_num]:
                    continue

                aview = views[v_num]
                adepth = depth[v_num]

                for x[v] in range(dims[v]):
                    for x[u] in range(dims[u]):

                        # March along ray
                        buf_idx = x[u] + x[v]*dims[u]
                        for x[d] in range(adepth[buf_idx], dims[d], s):

                            # Read volume color
                            vol_idx = x[0] + dims[0] * (x[1] + dims[1] * x[2])
                            color = volume[vol_idx]
                            if color == mask_color:
                                continue

                            color = volume[vol_idx] = aview[x[u] + dims[u] * x[v]]

                            # Check photoconsistency of volume at x
                            consistent = True
                            for a in range(3):
                                if not consistent:
                                    break

                                b = (a+1)%3
                                c = (a+2)%3
                                idx = x[b] + dims[b] * x[c]
                                for t in range(2):
                                    fnum = 2*a+t
                                    if skip[fnum]:
                                        continue
                                    fcolor = views[fnum][idx]
                                    fdepth = depth[fnum][idx]
                                    if (t and fdepth <= x[a]) or (not t and x[a] <= fdepth):
                                        if fcolor != color:
                                            consistent = False
                                            break
                            if consistent:
                                break

                            # Clear out voxel
                            removed += 1
                            volume[vol_idx] = mask_color

                        # Update depth value
                        adepth[buf_idx] = x[d]

    # Do a final pass to fill in any missing colors
    n = 0
    for x[2] in range(dims[2]):
        for x[1] in range(dims[1]):
            for x[0] in range(dims[0]):
                if volume[n] < 0:
                    volume[n] = 0xff00ff
                n += 1

    return {"volume": volume, "dims": dims}

