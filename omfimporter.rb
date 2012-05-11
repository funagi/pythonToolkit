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
		#UI.messagebox(file_path)
		file = File.new(file_path, "r")
		content = file.read
		#UI.messagebox(content)
		begin
			xmax = /(xnodes: )(\d+)/.match(content)[2]
			ymax = /(ynodes: )(\d+)/.match(content)[2]
			zmax = /(znodes: )(\d+)/.match(content)[2]
			datalist = /(# Begin: Data Text)((\w|\W)+)(# End: Data Text)/.match(content)[2]
			regex = /((-|)\d+.\d+(e(-|)\d+|))/
			datatable = datalist.scan(regex)
			arrow = Sketchup.active_model.definitions.load(
				Sketchup.find_support_file("arrow.skp", "Components/Components Sampler/"))
			for z in 0..zmax.to_i-1
				for y in 0..ymax.to_i-1
					for x in 0..xmax.to_i-1
						offset = 3*(z*ymax.to_i*xmax.to_i+y*xmax.to_i+x)
						px = datatable[offset][0].to_f
						#UI.messagebox(datatable[offset][0])
						py = datatable[offset+1][0].to_f
						pz = datatable[offset+2][0].to_f
						axis = Geom::Vector3d.new(
							px/Math.sqrt(2*pz+2),
							py/Math.sqrt(2*pz+2),
							Math.sqrt(0.5*pz+0.5)
							)
						point = Geom::Point3d.new(x*60,y*60,z*60)
						entities = Sketchup.active_model.entities
						group = entities.add_group();groupEnts = group.entities
 						#groupEnts.add_3d_text('X', TextAlignLeft, "Symbol",
 						#	true, false, 1.0, 0.0, 0.5, true, 0.1)
						groupEnts.add_instance(
							arrow, 
							Geom::Transformation.rotation([0,0,30],axis,3.14)
							)
 						group.move!(point)
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