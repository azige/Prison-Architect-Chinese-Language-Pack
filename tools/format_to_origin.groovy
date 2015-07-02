
def origin = new File("../data/language/base-language-alpha34.txt")
def target = new File("../data/language/base-language.txt")

def map = [:]

target.eachLine{
    def str = it.trim()
    if (str.size() < 1 || str[0] == '#'){
        return
    }
    
    def kv = str.split(/\s+/, 2)
    if (kv.size() > 1){
        map[kv[0]] = kv[1]
    }else{
        map[kv[0]] = "[TODO]"
    }
}

def sb = new StringBuilder()

origin.eachLine{
    def str = it.trim()
    if (str.size() < 1 || str[0] == '#'){
        sb << it << '\n'
        return
    }
    
    def kv = str.split(/\s+/, 2)
    if (map[kv[0]]){
        sb << String.format('%-40s', kv[0]) << map[kv[0]] << '\n'
    }else{
        sb << String.format('%-40s', kv[0]) << '[TODO]' << kv[1] << '\n'
    }
}

target.bytes = sb.toString().getBytes('UTF-8')
