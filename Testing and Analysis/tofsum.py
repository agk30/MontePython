import roi
import numpy
import os

output_directory = "Output Images/Summed Images/"

surface_list = ["SQA","SQE","IB","PFPE","OA"]
transition_list = ["Q11","Q12","Q13","Q14","Q15"]

print (os.path.isdir(output_directory))

if not os.path.isdir(output_directory):
    os.makedirs(output_directory)

for i in range(5):
    for j in range(5):
        if not os.path.isdir(output_directory+surface_list[i]+"/"+transition_list[j]):
            os.makedirs(output_directory+surface_list[i]+"/"+transition_list[j])

summed_image_pile, delay_list = roi.sum_tofs(r"E:\170122")

for i in range(5):
    for j in range(5):
        for k in range(len(delay_list)):
            with open(output_directory+surface_list[i]+"/"+transition_list[j]+"/"+delay_list[k], "w") as f:
                numpy.savetxt(f, summed_image_pile[:,:,i,j,k])