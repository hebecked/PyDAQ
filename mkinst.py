import os, sys


class instruction_maker(object):

	def __init__(self,filename=None,version=1):
		if version==1:
			self.version=version
			self.tasks=["#","wavelength","grating","filter","avrgn","readLockinr","readLockins","xpos","ypos","zpos","xyz_pos_type","vx","vy","vz","alpha","beta","gamma","rot_pos_type","delay"]
		else:
			raise ValueError('The version ' + str(version) + ' is not supportd')
		if filename!=None:
			self.file=files(filename)
		else:
			raise ValueError('Please define a filename')#
		header='# v=' + str(self.version) + ' Instruction file created with instruction_maker (by Dustin hebecker).\n'
		for task in self.tasks:
			header+=task + ' '
		header=header[0:-2]+'\n'
		self.file.init_file(header, override=True)
		self.count=0

	def add_instruction(self,wavelength=-1,grating=-1,filter_=-1,avrgn=10,readLockinr=False,readLockins=False,xpos=0,ypos=0,zpos=0,xyz_pos_type='idl',vx=-1,vy=-1,vz=-1,alpha=0,beta=0,gamma=0,rot_pos_type='idl',delay=0):
		'''Add new instructions. Default values will do nothing.'''
		line=''
		if self.version==1:
			if type(wavelength)!=int:
				raise ValueError(str(wavelength) +' is not of type int.')
			if type(grating)!=int:
				raise ValueError(str(grating) +' is not of type int.')
			if type(filter_)!=int:
				raise ValueError(str(filter_) +' is not of type int.')			
			if type(avrgn)!=int:
				raise ValueError(str(avrgn) +' is not of type int.')
			if type(readLockinr)!=bool:
				raise ValueError(str(readLockinr) +' is not of type bool.')
			if type(readLockins)!=bool:
				raise ValueError(str(readLockins) +' is not of type bool.')
			if type(xpos)!=int:
				raise ValueError(str(xpos) +' is not of type int.')
			if type(ypos)!=int:
				raise ValueError(str(ypos) +' is not of type int.')
			if type(zpos)!=int:
				raise ValueError(str(zpos) +' is not of type int.')
			if xyz_pos_type!='idl' and xyz_pos_type!='abs' and xyz_pos_type!='rel': 
				raise ValueError(str(xyz_pos_type) +' is not a valid xyz_pos_type.')
			if type(vx)!=int:
				raise ValueError(str(vx) +' is not of type int.')
			if type(vy)!=int:
				raise ValueError(str(vy) +' is not of type int.')
			if type(vz)!=int:
				raise ValueError(str(vz) +' is not of type int.')
			if type(alpha)!=float and type(alpha)!=int:
				raise ValueError(str(alpha) +' is not of type float.')
			if type(beta)!=float and type(beta)!=int:
				raise ValueError(str(beta) +' is not of type float.')
			if type(gamma)!=float and type(gamma)!=int:
				raise ValueError(str(gamma) +' is not of type float.')
			if rot_pos_type!='idl' and rot_pos_type!='abs' and rot_pos_type!='rel': 
				raise ValueError(str(rot_pos_type) +' is not a valid rot_pos_type.')
			if type(delay)!=float and type(delay)!=int:
				raise ValueError(str(delay) +' is not of type float.')
			line+=str(self.count)+' ' #"#"
			line+=str(wavelength)+' ' #"wavelength"
			line+=str(grating)+' ' #"grating"
			line+=str(filter_)+' ' #"filter"
			line+=str(avrgn)+' ' #"avrgn"
			line+=str(readLockinr)+' ' #"readLockinr"
			line+=str(readLockins)+' ' #"readLockins"
			line+=str(xpos)+' ' #"xpos"
			line+=str(ypos)+' ' #"ypos"
			line+=str(zpos)+' ' #"zpos"
			line+=str(xyz_pos_type)+' ' #"xyz_pos_type"
			line+=str(vx)+' ' #"vx"
			line+=str(vy)+' ' #"vy"
			line+=str(vz)+' ' #"vz"
			line+=str(alpha)+' ' #"alpha"
			line+=str(beta)+' ' #"beta"
			line+=str(gamma)+' ' #"gamma"
			line+=str(rot_pos_type)+' ' #"rot_pos_type"
			line+=str(delay)+' ' #"delay"
		self.file.append_line(line)
		self.count+=1