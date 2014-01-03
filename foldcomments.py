import sublime, sublime_plugin, re

class ToggleFoldCommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		comments = view.find_by_selector('comment')
		regions = []
		prev = None
		for region in comments:
			# multi_line = len(view.lines(region)) > 1
			# adjacent = prev and view.rowcol(prev.a)[0] == view.rowcol(region.a)[0]-1
			adjacent = self.adjacentComments(prev, region)

			# if not multi_line and adjacent:
			if adjacent:
				regions[-1] = regions[-1].cover(region)
			else:
				regions.append(region)
			prev = region
		
		regions = self.filter(regions)
		regions = map(lambda region: self.formatRegion(region), regions)

		self.toggle(regions)


	def adjacentComments(self, region_a, region_b):
		if not region_a or not region_b:
			return False
		view = self.view
		text = view.substr(sublime.Region(region_a.b, region_b.a))
		if re.search('\S', text) is None:
			return True
		return False


	def filter(self, regions):
		regions = filter(lambda region: self.inSelection(region), regions)
		regions = filter(lambda region: len(self.view.lines(region)) > 1, regions)
		return regions


	def formatRegion(self, region):
		view = self.view
		total_text = view.substr(region)
		res = re.search('\n', total_text)
		first_newline = res.start() if res is not None else 0
		start_a = region.a + first_newline
		end_b = region.b
		if total_text[-1] == '\n':
			end_b -= 1
		return sublime.Region(start_a, end_b)


	def inSelection(self, region):
		view = self.view
		selection = view.sel()
		if len(filter(lambda sel: not sel.empty(), selection)) == 0:
			return True
		for sel in selection:
			if region.intersects(sel):
				return True
		return False


	def toggle(self, regions):
		view = self.view
		if len(regions) > 0:
			if view.fold(regions[0]):
				view.fold(regions)
			else:
				view.unfold(regions)



# class ToggleFoldCommentsSelectionCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		view = self.view

# 		selection = view.sel()
# 		selected_regions = any_f(lambda region: not region.empty(), selection)

# 		comments = view.find_by_selector('comment')
# 		regions = []
# 		prev = None
# 		for region in comments:
# 			multi_line = len(view.lines(region)) > 1
# 			adjacent = prev and view.rowcol(prev.a)[0] == view.rowcol(region.a)[0]-1

# 			if not multi_line and adjacent:
# 				regions[-1] = regions[-1].cover(region)
# 			else:
# 				regions.append(region)
# 			prev = region

# 		if selected_regions:
# 			regions = filter(lambda region: any_f(lambda sel: region.intersects(sel), selection), regions)

# 		regions = filter(lambda region: len(view.lines(region)) > 1, regions)
# 		regions = [sublime.Region(region.a, region.b-1) if view.substr(region)[-1] == '\n' else region for region in regions]


# 		if len(regions) > 0:
# 			if view.fold(regions[0]):
# 				view.fold(regions)
# 			else:
# 				view.unfold(regions)

# def any_f(f, it):
# 	return len(filter(f, it)) > 0

