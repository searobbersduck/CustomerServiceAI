import tensorflow as tf
from tensorflow.python import pywrap_tensorflow
import fire

def get_tensors_from_checkpoint_file(file_name):
    varlist = []
    reader = pywrap_tensorflow.NewCheckpointReader(file_name)
    var_to_shape_map = reader.get_variable_to_shape_map()
    for key in sorted(var_to_shape_map):
        varlist.append(key)
    return varlist


def partial_transfer(checkpointPath):
    preTrainedVars = get_tensors_from_checkpoint_file(checkpointPath)
    allVars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
    restoreVars = []
    for v in allVars:
        name = v.name.encode("utf8")
        lastIdx = name.rfind(":")
        name = name[:lastIdx]
        if name.startswith("cls/title_out") or name.find("global_step")!= -1:
          print("======================skip %s....."%(name))
          continue
        if name in preTrainedVars:
            print("=====will restore:%s..."%(name))
            restoreVars.append(v)
    return tf.train.Saver(restoreVars)


def list_checkpoint(checkpointPath):
    preTrainedVars = get_tensors_from_checkpoint_file(checkpointPath)

    for name in preTrainedVars:
        print("=====%s"%(name))


if __name__ == "__main__":
    fire.Fire()
        