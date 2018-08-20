import os, shutil

word = 'word'
pos  = 'pos'
out  = 'out'
excluded = [out, os.path.basename(__file__)]
shutil.rmtree(out, ignore_errors = True)
os.makedirs(out, exist_ok = True)

for ngrsize in [x for x in os.listdir() if x not in excluded]:
		for vecsize in os.listdir(ngrsize):
				for s in [word, pos]:
					if int(vecsize) >= 5000 and s == pos: continue
					srcpath = f'{ngrsize}/{vecsize}/{s}.txt'
					dstpath = f'{out}/{ngrsize}_{s}_{vecsize}.txt'
					shutil.copy(srcpath, dstpath)
