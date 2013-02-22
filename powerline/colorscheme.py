# -*- coding: utf-8 -*-

DEFAULT_MODE_KEY = None
ATTR_BOLD = 1
ATTR_ITALIC = 2
ATTR_UNDERLINE = 4


class Colorscheme(object):
	def __init__(self, colorscheme_config):
		'''Initialize a colorscheme.'''
		self.colors = {}
		self.modes_groups = {DEFAULT_MODE_KEY: {}}

		# Create a dict of color tuples with both a cterm and hex value
		for color_name, color in colorscheme_config['colors'].items():
			try:
				self.colors[color_name] = (color[0], int(color[1], 16))
			except TypeError:
				self.colors[color_name] = (color, cterm_to_hex[color])

		# Create highlighting groups for all modes
		for group_name, group_props in colorscheme_config['groups'].items():
			group_attr_flag = self._get_attr_flag(group_props.get('attr', []))
			self.modes_groups[DEFAULT_MODE_KEY][group_name] = {
				'fg': self.colors[group_props['fg']],
				'bg': self.colors[group_props['bg']],
				'attr': group_attr_flag,
				}

			# Create mode-specific highlighting for this group
			for mode, translations in colorscheme_config.get('mode_translations', {}).items():
				if not mode in self.modes_groups:
					self.modes_groups[mode] = {}
				if group_name in translations.get('groups', {}):
					# Override entire group if present in the translations group dict
					self.modes_groups[mode][group_name] = {
						'fg': self.colors[translations['groups'][group_name]['fg']],
						'bg': self.colors[translations['groups'][group_name]['bg']],
						'attr': self._get_attr_flag(translations['groups'][group_name].get('attr', [])),
						}
				else:
					# Fallback to color translations from the translations colors dict
					self.modes_groups[mode][group_name] = {
						'fg': self.colors[translations.get('colors', {}).get(group_props['fg'], group_props['fg'])],
						'bg': self.colors[translations.get('colors', {}).get(group_props['bg'], group_props['bg'])],
						'attr': group_attr_flag,
						}

	def get_group_highlighting(self, group):
		'''Return highlighting information for all modes of a highlighting group.'''
		group_highlighting = {}
		for mode, mode_group in self.modes_groups.items():
			try:
				group_highlighting[mode] = mode_group[group]
			except TypeError:
				for try_group in group:
					if try_group in self.modes_groups[mode]:
						group_highlighting[mode] = mode_group[try_group]
						break
			finally:
				if mode not in group_highlighting:
					raise KeyError('Highlighting groups not found in colorscheme: {0}'.format(group))
		return group_highlighting

	def get_highlighting(self, group, mode=None):
		'''Return highlighting information for a highlighting group and mode.

		If no mode is specified, or the mode doesn't exist, highlighting for
		the default mode is returned.
		'''
		if not mode or mode not in self.modes_groups:
			mode = DEFAULT_MODE_KEY
		try:
			return self.modes_groups[mode][group]
		except TypeError:
			for try_group in group:
				if try_group in self.modes_groups[mode]:
					return self.modes_groups[mode][try_group]
			raise KeyError('Highlighting groups not found in colorscheme: {0}'.format(group))
		return self.modes_groups[mode][group]

	def _get_attr_flag(self, attributes):
		'''Convert an attribute array to a renderer flag.'''
		attr_flag = 0
		if 'bold' in attributes:
			attr_flag |= ATTR_BOLD
		if 'italic' in attributes:
			attr_flag |= ATTR_ITALIC
		if 'underline' in attributes:
			attr_flag |= ATTR_UNDERLINE
		return attr_flag

cterm_to_hex = {
	16: 0x000000, 17: 0x00005f, 18: 0x000087, 19: 0x0000af, 20: 0x0000d7, 21: 0x0000ff,
	22: 0x005f00, 23: 0x005f5f, 24: 0x005f87, 25: 0x005faf, 26: 0x005fd7, 27: 0x005fff,
	28: 0x008700, 29: 0x00875f, 30: 0x008787, 31: 0x0087af, 32: 0x0087d7, 33: 0x0087ff,
	34: 0x00af00, 35: 0x00af5f, 36: 0x00af87, 37: 0x00afaf, 38: 0x00afd7, 39: 0x00afff,
	40: 0x00d700, 41: 0x00d75f, 42: 0x00d787, 43: 0x00d7af, 44: 0x00d7d7, 45: 0x00d7ff,
	46: 0x00ff00, 47: 0x00ff5f, 48: 0x00ff87, 49: 0x00ffaf, 50: 0x00ffd7, 51: 0x00ffff,
	52: 0x5f0000, 53: 0x5f005f, 54: 0x5f0087, 55: 0x5f00af, 56: 0x5f00d7, 57: 0x5f00ff,
	58: 0x5f5f00, 59: 0x5f5f5f, 60: 0x5f5f87, 61: 0x5f5faf, 62: 0x5f5fd7, 63: 0x5f5fff,
	64: 0x5f8700, 65: 0x5f875f, 66: 0x5f8787, 67: 0x5f87af, 68: 0x5f87d7, 69: 0x5f87ff,
	70: 0x5faf00, 71: 0x5faf5f, 72: 0x5faf87, 73: 0x5fafaf, 74: 0x5fafd7, 75: 0x5fafff,
	76: 0x5fd700, 77: 0x5fd75f, 78: 0x5fd787, 79: 0x5fd7af, 80: 0x5fd7d7, 81: 0x5fd7ff,
	82: 0x5fff00, 83: 0x5fff5f, 84: 0x5fff87, 85: 0x5fffaf, 86: 0x5fffd7, 87: 0x5fffff,
	88: 0x870000, 89: 0x87005f, 90: 0x870087, 91: 0x8700af, 92: 0x8700d7, 93: 0x8700ff,
	94: 0x875f00, 95: 0x875f5f, 96: 0x875f87, 97: 0x875faf, 98: 0x875fd7, 99: 0x875fff,
	100: 0x878700, 101: 0x87875f, 102: 0x878787, 103: 0x8787af, 104: 0x8787d7, 105: 0x8787ff,
	106: 0x87af00, 107: 0x87af5f, 108: 0x87af87, 109: 0x87afaf, 110: 0x87afd7, 111: 0x87afff,
	112: 0x87d700, 113: 0x87d75f, 114: 0x87d787, 115: 0x87d7af, 116: 0x87d7d7, 117: 0x87d7ff,
	118: 0x87ff00, 119: 0x87ff5f, 120: 0x87ff87, 121: 0x87ffaf, 122: 0x87ffd7, 123: 0x87ffff,
	124: 0xaf0000, 125: 0xaf005f, 126: 0xaf0087, 127: 0xaf00af, 128: 0xaf00d7, 129: 0xaf00ff,
	130: 0xaf5f00, 131: 0xaf5f5f, 132: 0xaf5f87, 133: 0xaf5faf, 134: 0xaf5fd7, 135: 0xaf5fff,
	136: 0xaf8700, 137: 0xaf875f, 138: 0xaf8787, 139: 0xaf87af, 140: 0xaf87d7, 141: 0xaf87ff,
	142: 0xafaf00, 143: 0xafaf5f, 144: 0xafaf87, 145: 0xafafaf, 146: 0xafafd7, 147: 0xafafff,
	148: 0xafd700, 149: 0xafd75f, 150: 0xafd787, 151: 0xafd7af, 152: 0xafd7d7, 153: 0xafd7ff,
	154: 0xafff00, 155: 0xafff5f, 156: 0xafff87, 157: 0xafffaf, 158: 0xafffd7, 159: 0xafffff,
	160: 0xd70000, 161: 0xd7005f, 162: 0xd70087, 163: 0xd700af, 164: 0xd700d7, 165: 0xd700ff,
	166: 0xd75f00, 167: 0xd75f5f, 168: 0xd75f87, 169: 0xd75faf, 170: 0xd75fd7, 171: 0xd75fff,
	172: 0xd78700, 173: 0xd7875f, 174: 0xd78787, 175: 0xd787af, 176: 0xd787d7, 177: 0xd787ff,
	178: 0xd7af00, 179: 0xd7af5f, 180: 0xd7af87, 181: 0xd7afaf, 182: 0xd7afd7, 183: 0xd7afff,
	184: 0xd7d700, 185: 0xd7d75f, 186: 0xd7d787, 187: 0xd7d7af, 188: 0xd7d7d7, 189: 0xd7d7ff,
	190: 0xd7ff00, 191: 0xd7ff5f, 192: 0xd7ff87, 193: 0xd7ffaf, 194: 0xd7ffd7, 195: 0xd7ffff,
	196: 0xff0000, 197: 0xff005f, 198: 0xff0087, 199: 0xff00af, 200: 0xff00d7, 201: 0xff00ff,
	202: 0xff5f00, 203: 0xff5f5f, 204: 0xff5f87, 205: 0xff5faf, 206: 0xff5fd7, 207: 0xff5fff,
	208: 0xff8700, 209: 0xff875f, 210: 0xff8787, 211: 0xff87af, 212: 0xff87d7, 213: 0xff87ff,
	214: 0xffaf00, 215: 0xffaf5f, 216: 0xffaf87, 217: 0xffafaf, 218: 0xffafd7, 219: 0xffafff,
	220: 0xffd700, 221: 0xffd75f, 222: 0xffd787, 223: 0xffd7af, 224: 0xffd7d7, 225: 0xffd7ff,
	226: 0xffff00, 227: 0xffff5f, 228: 0xffff87, 229: 0xffffaf, 230: 0xffffd7, 231: 0xffffff,
	232: 0x080808, 233: 0x121212, 234: 0x1c1c1c, 235: 0x262626, 236: 0x303030, 237: 0x3a3a3a,
	238: 0x444444, 239: 0x4e4e4e, 240: 0x585858, 241: 0x626262, 242: 0x6c6c6c, 243: 0x767676,
	244: 0x808080, 245: 0x8a8a8a, 246: 0x949494, 247: 0x9e9e9e, 248: 0xa8a8a8, 249: 0xb2b2b2,
	250: 0xbcbcbc, 251: 0xc6c6c6, 252: 0xd0d0d0, 253: 0xdadada, 254: 0xe4e4e4, 255: 0xeeeeee,
	}
