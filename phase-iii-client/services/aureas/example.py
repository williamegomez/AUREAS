
import numpy as np
from utils.spectrogram_utils import SpectrogramUtils
from utils.feature_extraction_utils import FeatureExtractionUtils
from utils.classification_utils import ClassificationUtils
from constants.headers import headers_data, headers_data_no_display, headers_clusters, headers_clusters_no_display


def get_representative_calls(recon, data, metadata):
    unique_clusters = np.unique(recon)
    index_representative = np.zeros((unique_clusters.shape), dtype=int)
    representive_calls = list()

    for i, cluster in enumerate(unique_clusters):
        indices = np.where(recon == cluster)[0]
        calls = data[indices]
        mean_calls = np.mean(calls, axis=0)[None, :]
        distances = np.linalg.norm(calls - mean_calls, axis=1)
        index_representative[i] = np.argmin(distances)
        meta_representative = metadata[indices[index_representative[i]]]
        representive_calls.append([str(i), str(len(indices)), *(meta_representative[4:7].tolist()),
                                   str(np.around(np.mean(metadata[indices, 3].astype(
                                       float)), 2)), meta_representative[0],
                                   meta_representative[2], meta_representative[3]])
    return representive_calls


def process_files(directory, files):
    spectrogram_utils = SpectrogramUtils()
    feature_utils = FeatureExtractionUtils()

    total_features = np.array([])
    total_segs = np.array([])
    total_metadata = np.array([])
    for i, file in enumerate(files):
        segment_intervals, segs, f, t, s, metadata = spectrogram_utils.extract_complete_data(
            directory, file, 1)

        nc = 10
        nframes = 10
        nfilters = 30

        features, features_removed = feature_utils.extract_features(
            segs, nfilters, nc, nframes)
        segs = np.delete(np.array(segs), features_removed)[:, None]
        metadata = np.delete(np.array(metadata), features_removed, axis=0)
        metadata = np.around(metadata, 2)
        titles = np.tile(np.array([file]), (metadata.shape[0], 1))
        metadata = np.hstack((titles, metadata))

        if i == 0:
            total_features = total_features.reshape((0, features.shape[1]))
            total_segs = total_segs.reshape((0, segs.shape[1]))
            total_metadata = total_metadata.reshape((0, metadata.shape[1]))

        total_features = np.vstack((total_features, features))
        total_segs = np.vstack((total_segs, segs))
        total_metadata = np.vstack((total_metadata, metadata))

    return total_features, total_segs, total_metadata


directory = '/Users/williamgomez/Downloads/Colostethus fraterdanieli/Entrenamiento/'
files = ['JAGUAS260_20121120_064500.wav']
features, segs, metadata = process_files(directory, files)

classification_utils = ClassificationUtils()

ex_level = 1
it_num = 5
data = np.hstack((features, metadata[:, 6].astype(float)[:, None]))
mad = 'binomial'
gad = '3pi'

datanorm, mininums, maximums = classification_utils.norm(data)
recon, mean_class, std_class = classification_utils.lamda(
    ex_level, it_num, datanorm, mad, gad)

representive_calls = get_representative_calls(
    recon, datanorm, metadata)

keys_results = [header['label'] for header in headers_data]
keys_clusters = [header['label'] for header in headers_clusters]
keys_results_no_display = [header['label']
                           for header in headers_data_no_display]
keys_clusters_no_display = [header['label']
                            for header in headers_clusters_no_display]

data_results = []
for i, value in enumerate(metadata):
    values = [value[0], str(recon[i]), *
              (value[1:].tolist()), datanorm[i]]
    zipbObj = zip(keys_results + keys_results_no_display, values)
    data_results.append(dict(zipbObj))

data_clusters = []
for i, value in enumerate(representive_calls):
    zipbObj = zip(keys_clusters + keys_clusters_no_display, value)
    data_clusters.append(dict(zipbObj))
