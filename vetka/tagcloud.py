import sys


def tagcloud(taglist):
    # [('tag0',count0),('tag1',count1), ...]
    (tags, minv, maxv) = getSortedTags(taglist)
    if maxv - minv < 2:
        print('cloud0')
        cloud = getCloud0(tags)
        size = 0
    else:
        if len(tags) < 8:
            print('cloud3')
            cloud = getCloud3(tags, minv, maxv)
            size = 3
        elif len(tags) < 16:
            print('cloud5')
            cloud = getCloud5(tags, minv, maxv)
            size = 5
        else:
            print('cloud7')
            cloud = getCloud7(tags, minv, maxv)
            size = 7
    return size, cloud


def readTagsFromFile(inputfile):
    inputf = open(inputfile, 'r')
    taglist = {}
    while True:
        line = inputf.readline()[:-1]
        if line == '':
            break

        tag = taglist.get(line)
        if tag is None:
            taglist[line] = 1
        else:
            taglist[line] += 1
    return taglist


def getSortedTags(taglist):
    tags = []
    maxv = 0
    minv = sys.maxsize
    for t in taglist:
        v = taglist[t]
        if v > maxv:
            maxv = v
        elif v < minv:
            minv = v
        tags.append((t, v))
    tags.sort(key=lambda x: x[0].name.lower())
    return tags, minv, maxv


def getCloud0(tags):
    cloud = []
    for t in tags:
        cloud.append((t[0], 0))
    return cloud


def getCloud7(tags, minv, maxv):
    delta = (maxv - minv) / 7
    cloud = []
    for t in tags:
        tag = t[0]
        val = 0
        cnt = t[1]
        if cnt < minv + delta:
            val = -3
        elif cnt < minv + 2 * delta:
            val = -2
        elif cnt < minv + 3 * delta:
            val = -1
        if cnt >= maxv - delta:
            val = 3
        elif cnt >= maxv - 2 * delta:
            val = 2
        elif cnt >= maxv - 3 * delta:
            val = 1
        cloud.append((tag, val))
    return cloud


def getCloud5(tags, minv, maxv):
    delta = (maxv - minv) / 5
    cloud = []
    for t in tags:
        tag = t[0]
        val = 0
        cnt = t[1]
        if cnt < minv + delta:
            val = -2
        elif cnt < minv + 2 * delta:
            val = -1
        if cnt >= maxv - delta:
            val = 2
        elif cnt >= maxv - 2 * delta:
            val = 1
        cloud.append((tag, val))
    return cloud


def getCloud3(tags, minv, maxv):
    delta = (maxv - minv) / 3
    cloud = []
    for t in tags:
        tag = t[0]
        val = 0
        cnt = t[1]
        if cnt < minv + delta:
            val = -1
        if cnt >= maxv - delta:
            val = 1
        cloud.append((tag, val))
    return cloud
