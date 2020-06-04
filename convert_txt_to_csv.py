import numpy as npy

dataset=npy.loadtxt("Email-Enron.txt", dtype=int)
print(dataset.shape)
#delete duplication
#dataset=npy.vstack({tuple(row) for row in npy.sort(dataset)})
#npy.savetxt("CA-HepTh.csv", npy.vstack({tuple(row) for row in dataset}), fmt="%i", delimiter=',')
npy.savetxt("Email-Enron.csv", dataset, fmt="%i", delimiter=',')
print(dataset.shape)
