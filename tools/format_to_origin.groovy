
@groovy.transform.SourceURI sourceURI
def baseDir = new File(sourceURI).parentFile
def origin = new File(baseDir, "../data/language/base-language-origin.txt")
def targets = [
    new File(baseDir, "../data/language/base-language.txt"),
    new File(baseDir, "../official-simplifiedchinese/base-language.txt")
]
targets.each{ target ->
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
        
        def matcher = str =~ /(\w+)(\s+)(.+)/
        def key = matcher[0][1]
        def space = matcher[0][2]
        def value = matcher[0][3]
        if (map[key]){
            sb << key << space << map[key] << '\n'
        }else{
            sb << key << space << '[TODO]' << value << '\n'
        }
    }

    target.bytes = sb.toString().getBytes('UTF-8')
}