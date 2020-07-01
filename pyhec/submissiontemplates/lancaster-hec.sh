#$ -S /bin/bash
# Template file for Lancaster University's HEC

#$ -N pyHEC_submission
#$ -q serial

# Run the job on x nodes with 16 cores each
#$ -l node_type=40core192G
#$ -l h_vmem=50G

# Send email notification after completion
#$ -m e
#$ -M foo@example.com

source /etc/profile
module add anaconda3/2019.07
python "$1"
