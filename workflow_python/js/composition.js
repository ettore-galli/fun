

function Composer(f) {
    return {
        map: function (g) {
            return x => g(f(x));
        },
        execute: function (x) {
            return f(x);
        }
    }
}

 


async function main() {
    console.log("========== COMPOSITION ==========");
    const x = await Promise.resolve(3);
    const y = await Promise.resolve(2);
    console.log(x + y)  


}

function* coso(){
    yield 3.1515;
    yield await Promise.resolve(2);
}
function genemain(){
    const c = coso();
    console.log(c.next().value)
    console.log(c.next().value)
}

main();
genemain();