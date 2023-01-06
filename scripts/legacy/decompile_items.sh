#!/bin/bash

if ! command -v py &>/dev/null; then
    echo "Cannot proceed without a python 3 installation!"
    exit 1
fi


export i18n="C:/Users/33630/AppData/Local/Ankama/Dofus/data/i18n/"
export common="C:/Users/33630/AppData/Local/Ankama/Dofus/data/common/"
export elements="C:/Users/33630/AppData/Local/Ankama/Dofus/content/maps/elements.ele"
export maps="C:/Users/33630/AppData/Local/Ankama/Dofus/content/maps/"

export pydofusPath="C:/Users/33630/Desktop/PyDofus/PyDofus"
export sourcesPath="C:/Users/33630/Desktop/mitm/mitm_d2/sources"


##############################################
##############################################
##############################################

# rm "$pydofusPath/output/"*"/"*"/"*".dlm"
# cp "$pydofusPath/output/"* "$sourcesPath/data/maps"
# exit 0;

# if [ ! -d "../../sources/data" ]; then
#     mkdir -p "../../sources/data";
# else
#     rm "../../sources/data/"*
# fi
# if [ ! -d "./input" ]; then
#     mkdir -p "./input";
# fi
# if [ ! -d "./output" ]; then
#     mkdir -p "./output";
# fi

##############################################
##############################################
##############################################

cd 
rm -rf "$pydofusPath/input/"*
rm -rf "$pydofusPath/output/"*

rm -rf "$sourcesPath/data/maps/"*
rm -rf "$sourcesPath/data/common/"*
rm -rf "$sourcesPath/data/elements/"*

# First do the i18n file

#  echo "Decompiling internationalisation files..."
# cp "$i18n"*.d2i "$pydofusPath/input"
# for file in  "$pydofusPath/input/"*".d2i"; do
#      py "$pydofusPath/d2i_unpack.py" "$file"
# done

# cp "$pydofusPath/input/"*".json" "$sourcesPath/data/i18n"

# # Then all the d2o files

# echo "Decompiling object files..."

# cp "$common"*.d2o "$pydofusPath/input"
# py "$pydofusPath/d2o_unpack.py"
# mv "$pydofusPath/output/"* "$sourcesPath/data/common"
# rm -rf "$pydofusPath/input/"*

# Finally the map files:


echo "Decompiling map files..."

# echo "Map files are huge and take a long time to decompile (~40minutes). Do you want to decompile them now? (y/n)"

# read -r answer

# while [[ $answer != "y" && $answer != "n" ]] ; do
#   echo "Please answer (y)es or (n)o"
#   read -r answer
# done;

# if [[ $answer == "n" ]]; then
#   exit 0;
# fi;

py "$pydofusPath/ele_unpack.py" "$elements"
cp "${elements/.ele/.json}" "$sourcesPath/data/elements"

cp "$maps"*".d2p" "$pydofusPath/input/"
py "$pydofusPath/d2p_unpack.py"

for file in "$pydofusPath/output/"*"/"*"/"*".dlm"; do
  py "$pydofusPath/dlm_unpack.py" "$file"
done; 
rm "$pydofusPath/output/"*"/"*"/"*".dlm"
cp -r "$pydofusPath/output/"* "$sourcesPath/data/maps"


