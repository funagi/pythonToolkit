class OMFImporter < Sketchup::Importer

	def description
		return "OOMMF Oxsii Field File (*.omf)"
	end

	def file_extension
		return "omf"
	end

	def id
		return "com.sketchup.importers.oommf"
	end

	def support_options?
		return false
	end

	def load_file(file_path, status)

		#draw basic information
		file = File.new(file_path, "r")
		content = file.read
		begin
			xmax = /(xnodes: )(\d+)/.match(content)[2]
			ymax = /(ynodes: )(\d+)/.match(content)[2]
			zmax = /(znodes: )(\d+)/.match(content)[2]
			zslice = UI.inputbox(["Please input Z-Slice (0~"+(zmax.to_i-1).to_s+"):"])
			znum = zslice[0].to_i
			if znum==-1
				zmin=0
			else
				zmin=znum
				zmax=(znum+1).to_s
			end
		file.close

		lines = IO.readlines(file_path)
		offset = nil
		maxvalue = nil
		lines.each do |line|
			if line.index("ValueRangeMaxMag")!=nil
				maxvalue = /(# ValueRangeMaxMag: )(\d+(.\d+|))(\n)/.match(line)[2]
			end
			if line.index("Begin: Data Text")!=nil
				offset = lines.index(line)+1
				break
			end
		end
		#draw sth.
		arrow = Sketchup.active_model.definitions.load(
				Sketchup.find_support_file("arrow.skp", "Components/Components Sampler/"))
		entities = Sketchup.active_model.entities
		group = entities.add_group();
		for z in zmin..zmax.to_i-1
			for y in 0..ymax.to_i-1
				for x in 0..xmax.to_i-1
					line = lines[offset+z*xmax.to_i*ymax.to_i+y*ymax.to_i+x]
					datatable = line.scan(/((-|)\d+(\.\d+|)(e(-|)\d+|))/)
					#UI.messagebox(lines[offset+z*xmax.to_i*ymax.to_i+y*ymax.to_i+x])
					px = datatable[0][0].to_f/maxvalue.to_f
					py = datatable[1][0].to_f/maxvalue.to_f
					pz = datatable[2][0].to_f/maxvalue.to_f
					
					if px==0 && py==0 && pz==0
						next
					end
					
					axis = Geom::Vector3d.new(
						px/Math.sqrt(2*pz+2),
						py/Math.sqrt(2*pz+2),
						Math.sqrt(0.5*pz+0.5)
						)
					#UI.messagebox("#{datatable[0][0]} #{datatable[1]} #{datatable[2]} \n #{axis}")
					point = Geom::Point3d.new(x*60,y*60,z*60)
					groupEnts = group.entities
					inst = groupEnts.add_instance(
						arrow, 
						Geom::Transformation.rotation([0,0,27.4],axis,3.14)
						)
					inst.move!(point)
					trans = inst.transform! Geom::Transformation.rotation([x*60,y*60,z*60+27.4],axis,3.14)
				end
			end
		end

		rescue => err
			UI.messagebox(err)
			UI.messagebox()
			return 1
		end
		return 0
	end
end

Sketchup.register_importer(OMFImporter.new)