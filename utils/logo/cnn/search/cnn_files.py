from utils.files.file_utils import CnnFileUtils


class TrainingFile(CnnFileUtils):
    """Files and directories for trained, training,
        validation and test data and parameters"""

    def __init__(self):
        super(TrainingFile, self).__init__('search')


files = TrainingFile()
