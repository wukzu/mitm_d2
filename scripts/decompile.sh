#!/bin/sh

export DofusInvoker="C:/Users/llegay/Documents/DofusInvoker.swf"
export selectclass='com.ankamagames.dofus.BuildInfos,com.ankamagames.dofus.network.++,com.ankamagames.jerakine.network.++'
export config='parallelSpeedUp=0'

cd "$( dirname "${BASH_SOURCE[0]}" )"

./ffdec.sh \
  -config "$config" \
    -selectclass "$selectclass" \
      -export script \
        ./sources $DofusInvoker

sh ffdec.sh -config parallelSpeedUp=0 -selectclass com.ankamagames.dofus.BuildInfos,com.ankamagames.dofus.network.++,com.ankamagames.jerakine.network.++ -export script ../sources C:/Users/llegay/Documents/DofusInvoker.swf
sh ffdec.sh -config parallelSpeedUp=0 -selectclass com.ankamagames.dofus.BuildInfos,com.ankamagames.dofus.network.++,com.ankamagames.jerakine.network.++ -export script ../sources C:/Users/33630/Desktop/DofusInvoker.swf