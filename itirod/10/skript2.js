var str_in = `ааааабббббвввввгггггдддддаааааббвгааааа`
var str_out = ``
var mydictionary = {}
var mydictionary_bit = {}
var mass_key = []
var mass_value = []
var pos1_min = 0
var pos2_min = 0
var max_len = 0

for (let i = 0; i < str_in.length; i++) {
	if (mydictionary[str_in[i]] == undefined) {
		mydictionary[str_in[i]] = 1
		mydictionary_bit[str_in[i]] = ``
	} else {
		mydictionary[str_in[i]]++
	}
}

createmass(mass_key, mass_value, mydictionary)
srt(mass_value, mass_key)
createtree(mass_key, mass_value)
number_code(mydictionary_bit)
console.log(makestr_out(str_in, mydictionary_bit, max_len))

function createmass(m_k, m_v, dct) {
	let length = 0
	for (let key in dct) {
        m_k[length] = key
        m_v[length] = dct[key]
        length++
    }
}

function createtree(m_k_res, m_v_res) {
	let n = m_v_res.length
	while(n != 1) {
		searchtwomin(m_v_res)
		let s1 = m_k_res[pos1_min]
		for (let i = 0; i < s1.length; i++) {
			mydictionary_bit[s1[i]] += `1`
		}
		let s2 = m_k_res[pos2_min]
		for (let i = 0; i < s2.length; i++) {
			mydictionary_bit[s2[i]] += `0`
		}
		m_v_res[pos2_min] += m_v_res[pos1_min]
		m_k_res[pos2_min] += m_k_res[pos1_min]
		m_v_res.splice(pos1_min, 1)
		m_k_res.splice(pos1_min, 1)
		n--
	}
}

function srt(mass1, mass2) {
	let n = mass1.length
	for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - 1 - i; j++) {
            if (mass1[j + 1] > mass1[j]) {
                [ mass1[j + 1], mass1[j], mass2[j + 1], mass2[j] ] = [ mass1[j], mass1[j + 1], mass2[j], mass2[j + 1] ]
            }
        }
    }
}

function number_code(dict_code) {
	let res = ``
	for (let key in dict_code) {
		[ res, dict_code[key] ] = [ dict_code[key], `` ]
		for (let i = res.length - 1; i >= 0; i--) {
			dict_code[key] += res[i]
		}
		if (max_len < res.length) {
			max_len = res.length
		}
    }
}

function searchtwomin(m) {
	let n = m.length
	pos1_min = n - 1
	for (let i = n - 2; i >= 0; i--) {
		if (m[pos1_min] > m[i]) {
			pos1_min = i
		}
	}
	if (pos1_min == n - 1) {
		pos2_min = n - 2
		n -= 1
	} else {
		pos2_min = n - 1
	}
	for (let i = n - 2; i >= 0; i--) {
		if (m[pos2_min] > m[i] && i != pos1_min) {
			pos2_min = i
		}
	}
	if (pos1_min < pos2_min) {
		[ pos1_min, pos2_min ] = [ pos2_min, pos1_min ]
	}
}

function makestr_out(s_in, mydictionary_bit, max_len) {
	let s_out = ``
	let code = ``
	let ch = ``
	for (let i = 0; i < s_in.length; i++) {
		ch = s_in[i]
		code = mydictionary_bit[ch]
		if (code.length < max_len) {
			for (let j = 0; j < max_len - code.length; j++) {
				s_out += `0`
			}
		}
		s_out += `${code} `
	}
	return s_out
}
