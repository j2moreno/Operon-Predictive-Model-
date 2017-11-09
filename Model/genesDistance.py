import sys 
import MySQLdb

#connects to SQL database
db = MySQLdb.connect(host="bm185s-mysql.ucsd.edu",user="j2moreno", passwd="Azsxdcf1", db="j2moreno_db")  
cursor = db.cursor()
curr = db.cursor()

#reads the files of genes inside operon 
filename = sys.argv[1] 
file = open(filename, 'r')

data = file.readlines()
array = []

for element in data:
  element = element.replace('\n', '')
  array.append(element)

#read the genes.txt file which has the gene name and its corresponding locus tag
filename = sys.argv[2] 
file2 = open(filename,'r')
data = file2.readlines()
geneDict = dict()

#creates the dictionary that matches a gene to its locus tag
for element in data:
  element = element.replace('\n', '')
  element = element.split('\t')
  geneDict[element[0]] = element[1]

counter= 0 
mutipleOperonGenes = []
distances = []

#For every element in the genes.txt file
for element in array:
  element = element.split(',')
  leftDist = 0
  rightDist = 0
  dist = 0

  #if muti-gene in operon 
  if len(element) > 1:
    
    ToAdd = []
    for element2 in element:
      cursor.execute('''SELECT * from realGenes WHERE name=%s''', (element2,))
      row = cursor.fetchone()
      if row == None:
        if element2 in geneDict.keys():
          locus = geneDict[element2]
          if locus == None:
            continue
          curr.execute('''SELECT * from realGenes WHERE locus_tag=%s''', (locus,)) 
          row2 = curr.fetchone()
          if row2 == None:
            continue
          geneID = row2[0]
      else:
        geneID = row[0]
      
      cursor.execute('''SELECT * from exons WHERE gene_id=%s''', (int(geneID),))
      row = cursor.fetchone()
      if element2 == element[0]:
        rightDist = int(row[3])
        continue
      leftDist = int(row[2])
      
      dist = leftDist - rightDist
      rightDist = int(row[3])
      print dist

  #mono-genes
  else:
    cursor.execute('''SELECT * from realGenes WHERE name=%s''', (element[0],))
    row = cursor.fetchone()

    if row == None:
      if element[0] in geneDict.keys():
        locus = geneDict[element[0]]
        if locus == None:
          continue
        curr.execute('''SELECT * from realGenes WHERE locus_tag=%s''', (locus,)) 
        row2 = curr.fetchone()
        if row2 == None:
          continue
        geneID = row2[0]
    else:
      geneID = row[0]

    cursor.execute('''SELECT * from exons WHERE gene_id=%s''', (int(geneID),)) 
    row = cursor.fetchone()
    dist = 0
    print dist




