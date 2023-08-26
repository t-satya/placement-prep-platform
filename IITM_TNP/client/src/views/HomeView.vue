<script setup>
import { useStore } from 'vuex';
import { computed } from 'vue';

const store = useStore();

const loggedIn = computed(() => store.getters.get_login_status);


function login() {
  store.dispatch("loginUser")
}
function logout() {
  store.dispatch("logoutUser")
}

</script>

<template>
  Hello
  You are loggedIn : {{ loggedIn }}
  <div v-if="!loggedIn"><button @click="login">Login</button></div>
  <div v-else><button @click="logout">Logout</button></div>

  <div>
    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quia tempora ex quam incidunt ipsa sunt alias eius
    expedita. Ratione quaerat magnam, consectetur perspiciatis enim eum, ut accusantium neque dolore laboriosam ea
    suscipit veniam. Id recusandae, beatae a tenetur unde cupiditate ratione, eligendi aut obcaecati rerum autem natus
    minima, labore commodi repellat quos. Rem illo sit aut ea doloremque distinctio debitis ut aperiam, numquam suscipit
    molestias amet totam, animi ex culpa voluptates soluta, nemo quidem? Aut delectus quae accusantium voluptatibus
    minus vel earum quo error ut neque repellendus fuga incidunt natus accusamus aperiam laboriosam ab veritatis,
    quaerat eaque. Quibusdam quisquam libero unde ipsa corporis. Eveniet vitae, natus tempora facere totam quam animi
    suscipit omnis nihil, harum, cumque iusto quibusdam impedit quos fugit assumenda dolorem. Aspernatur dolorum
    veritatis eaque et quam, cum rerum, repellendus aperiam praesentium itaque culpa. Voluptatum inventore aut ad,
    debitis placeat obcaecati quis dolorum ea, vel ipsum sequi temporibus harum totam nemo fuga nisi quia labore
    dignissimos id rerum pariatur perspiciatis. Quae, eligendi dolorem corrupti incidunt impedit magni consectetur
    perferendis fugiat facere hic non, molestias quas! Rerum quo neque perspiciatis doloribus fugiat, deserunt cum
    voluptates totam molestiae veritatis doloremque, animi quibusdam consequatur quisquam sint assumenda atque! Vero,
    reiciendis! Voluptatum laudantium voluptate officiis eaque, natus id assumenda? Natus quidem porro exercitationem
    maxime, officiis eveniet voluptatum modi id animi, ratione dolore mollitia in? Beatae culpa at nihil nostrum
    recusandae? Delectus corporis, nihil impedit voluptates temporibus enim culpa similique eligendi quae voluptatibus
    explicabo quod alias porro autem qui, aspernatur deserunt ea illo incidunt cum. Sequi maxime quisquam at deleniti
    est! Quam repudiandae provident esse. Atque, veniam odit, libero aut, alias a consectetur ratione facilis unde nihil
    aliquam eum! Nobis dignissimos dolor maiores ad culpa minus quis similique aspernatur dolorem fuga recusandae
    accusamus consequatur eveniet veritatis corporis itaque tempore, tempora, laborum dolorum, odio animi. Culpa quod
    delectus, optio assumenda magnam, temporibus ab, velit totam sunt rem dolor iure mollitia voluptas quasi soluta
    ratione aut tempora inventore voluptatibus reprehenderit suscipit sint dolores. Sapiente dolore facilis nulla
    mollitia assumenda, exercitationem laudantium eaque illum? Placeat error, laudantium commodi quam, dicta est
    provident iste ducimus maiores sed, laboriosam voluptas ut alias dolorem repudiandae facilis. Reprehenderit omnis
    inventore, quos aliquid rerum, blanditiis quod facere maxime mollitia incidunt similique corporis quis sequi dolor
    voluptatem laudantium at explicabo quia quae nam! Ipsa animi molestiae ex rem eaque iure dicta tenetur, vitae veniam
    doloribus libero cumque quas perspiciatis iusto itaque fugit explicabo corporis sit maiores debitis. Quae
    perspiciatis debitis iste illo velit adipisci itaque? Animi voluptates veritatis eos cupiditate perspiciatis ex enim
    aliquid? Nisi eos quas culpa. Molestiae libero dolorem deleniti exercitationem delectus! Deserunt accusantium
    architecto quo nemo sed, eveniet sapiente maiores ipsam voluptate consequatur earum id, voluptates ratione eligendi?
    Culpa facilis velit ipsum. Tenetur facilis vero nihil eius iste nemo officia laudantium recusandae odit quis, iure
    ipsa veritatis est atque quasi sed assumenda praesentium eligendi in earum corporis. Perferendis iure molestias
    omnis quae dolorum obcaecati quasi laboriosam totam unde quidem. Aliquid dolor impedit nam provident soluta,
    incidunt eveniet error excepturi dolorum ab totam aspernatur, sequi distinctio est repellat dolorem minima dolores
    quasi. Vero enim, quos vitae illum quidem dicta! Laudantium, molestias omnis esse quibusdam perferendis soluta
    perspiciatis porro cumque fuga. Sint exercitationem explicabo assumenda ea ullam provident tenetur, qui doloremque,
    quas sunt ipsa ex odio porro ipsum eaque iusto neque quibusdam error. Tempora, adipisci. Earum harum odit, aliquid
    nesciunt explicabo eos. Commodi, vitae illo velit, dolor sequi fugiat voluptatem soluta quam porro tempore aliquam
    rerum incidunt doloribus beatae maxime culpa possimus officia, blanditiis quod quidem reprehenderit nam voluptatum
    reiciendis! Nemo, consequatur tempore asperiores quis saepe praesentium itaque ullam facere quos unde corrupti est
    ea ipsa a numquam in tenetur sunt, similique eveniet enim possimus harum recusandae dicta! Distinctio repudiandae,
    ullam vitae quae eos perspiciatis non facere deleniti, quo possimus doloremque provident, cumque repellendus.
    Voluptates ea accusamus in dolorem itaque laborum impedit placeat non reprehenderit beatae, sequi assumenda
    provident deleniti? Beatae laboriosam nesciunt ab sapiente voluptates non, aliquid omnis sed veniam itaque
    blanditiis maiores porro atque repudiandae voluptatem facere, accusamus dolores illum asperiores, pariatur odit eius
    debitis. Earum numquam ipsam similique architecto consequuntur adipisci est ea voluptate nemo sequi nostrum
    accusamus, culpa quas nesciunt laborum repudiandae nisi blanditiis. Temporibus quisquam, quae accusantium vitae
    voluptates vel adipisci nihil animi, dolorem dolor soluta non corporis minima tempore ipsam in dolores a eos quia.
    Vero necessitatibus, hic enim minima id veritatis adipisci exercitationem voluptas, fuga non sit. Officia vero unde,
    deleniti at enim voluptas amet quia eum. Quis ipsum culpa illo, nihil minima impedit. Atque est perspiciatis,
    corporis necessitatibus quod dolore ducimus iure corrupti vitae itaque numquam? Vitae fugit aut, at voluptatem
    dolores eaque rerum dicta esse nostrum repellat possimus odit illo earum laboriosam, quas exercitationem veniam
    facilis natus repellendus hic. Voluptates, itaque at. Blanditiis, et in quod ullam totam est facilis quo odit quos
    non, id sunt aperiam recusandae obcaecati odio officiis dolores quisquam, accusamus sequi aut exercitationem.
    Perferendis soluta odit assumenda impedit. In eaque sequi obcaecati sunt! Iste minus eum quo iusto quia excepturi
    deleniti veniam ab velit. Distinctio omnis quae ut sunt ipsam! Natus veniam autem, dolores ab impedit neque nobis
    mollitia hic excepturi. Optio cumque illo ad ipsa temporibus, enim distinctio in ex sapiente quidem suscipit aliquid
    nesciunt eveniet, ipsum doloribus similique neque minima quaerat asperiores laudantium, dolores perferendis quia
    molestias porro. Doloribus, iusto, atque quos nihil amet dolor molestias aspernatur eius sapiente unde reiciendis
    maxime tempore. Velit ea quasi ipsum inventore, a dolores, molestiae sed error quam hic eaque distinctio magnam
    asperiores animi exercitationem quaerat et, minima voluptates laboriosam. Nostrum vel reiciendis, dolorum unde quis
    perspiciatis sunt incidunt autem rem, dolore illo nisi. Perspiciatis iusto odit eos voluptatibus sequi in? Mollitia
    asperiores reprehenderit accusamus officia, dignissimos aperiam velit eveniet pariatur, amet sunt sint minus omnis
    praesentium doloremque voluptates! Obcaecati, consectetur quasi! Laborum, dolorem unde nihil laudantium doloremque
    vitae excepturi corrupti id cupiditate magni exercitationem voluptatibus asperiores magnam, ratione in odit
    consequatur corporis omnis, consequuntur quisquam minus odio? Consequuntur sapiente sint culpa vero, totam quidem
    blanditiis ea doloremque, rem vel iusto explicabo, dicta molestias provident similique architecto quam ipsa
    laudantium excepturi. Officia beatae sint, numquam nobis saepe cupiditate obcaecati? Obcaecati accusamus molestias
    blanditiis temporibus dolores natus in dolorem facilis sequi recusandae autem voluptatum repudiandae corrupti quia
    consequuntur illum officiis repellendus rem explicabo dolor beatae, ratione itaque nam. Similique animi architecto,
    iusto incidunt quisquam saepe dolore ipsa eaque praesentium quidem corporis voluptates at porro eveniet in unde est
    laudantium neque hic dicta, itaque ipsam. Perspiciatis, aut, consectetur neque vitae adipisci cum debitis obcaecati
    alias voluptas reiciendis esse in dolores quasi! Rerum ad, quaerat vitae minima quibusdam iure itaque harum magni
    assumenda sequi facilis, necessitatibus quas delectus blanditiis atque temporibus animi excepturi hic nisi dolor
    molestiae, quia at? Ipsum aliquam obcaecati possimus fugit eveniet, maxime totam iusto expedita voluptatem labore
    magni eaque officiis deserunt enim sint amet incidunt est ex dicta! Ut dolorem velit id in veniam delectus aut
    necessitatibus eius ducimus praesentium ad ipsum fugiat a, eum aperiam soluta sit maiores, recusandae laboriosam,
    dolores placeat assumenda accusantium. Exercitationem omnis itaque quod! Incidunt magnam ab laboriosam debitis quas
    illum libero veritatis saepe iusto nobis ipsa, quae sapiente corrupti dolores delectus temporibus quam laudantium
    voluptas. Illum earum nihil nam! Repudiandae, possimus illo suscipit saepe optio quibusdam fugit eum facilis, amet
    obcaecati, facere consequatur adipisci? Labore dignissimos, quas perferendis sunt est assumenda explicabo iste
    blanditiis aspernatur beatae eaque maxime tenetur aliquid incidunt in. Sed corporis enim rem qui officiis rerum ipsa
    commodi repudiandae cum ipsam sit expedita facilis repellat accusamus ab voluptates, atque totam veniam optio, natus
    iste amet! Eius magnam quod, quidem ratione autem, inventore facilis commodi obcaecati nisi laudantium repellendus
    quisquam non mollitia ipsa facere qui enim maiores provident rem officiis? Nihil iure nulla tempore illo optio quos
    minima nam amet? Harum tenetur repellat fugit modi cupiditate error et, corrupti eligendi voluptate perspiciatis
    consequatur iure neque accusantium doloribus? Ea aut nisi rerum ipsa magnam eos ullam reiciendis, magni placeat ad
    totam iusto fugiat mollitia libero vero corporis ipsam error excepturi ducimus a eveniet saepe unde. Quae temporibus
    assumenda ipsam laborum necessitatibus vitae molestiae accusamus quod animi autem suscipit perferendis officia
    distinctio eaque iste nemo culpa ipsum ullam illo praesentium soluta, veniam at sunt! Esse quis ipsam, voluptas
    nihil quae a sit fugit ut obcaecati, cumque enim officia. Nihil magni quos qui nemo, nobis voluptates? Minus
    consectetur iste reprehenderit, maiores architecto dicta cum earum nemo sapiente fugit. Eos sed, facilis ad delectus
    debitis tempora, ratione at illo nostrum provident dolorum odit animi nemo veritatis incidunt ullam quidem sequi
    reiciendis culpa! Totam eum sit quia odio tempore culpa ea, quas dolores amet enim voluptatum non labore
    consequuntur harum, sunt quibusdam ab ipsum minus nemo quam. Praesentium suscipit mollitia modi sequi temporibus vel
    ut est. Itaque sapiente architecto omnis harum quisquam doloribus recusandae provident corrupti ratione, quis
    dolorem accusantium quibusdam, amet hic sit reiciendis id quidem! Dicta dignissimos, nesciunt in velit rerum
    voluptatum ea quibusdam fuga libero dolorem reiciendis modi quasi animi. Inventore eaque recusandae repudiandae
    dolores qui consectetur eveniet voluptatibus animi fugiat, laborum rem eos quia cum distinctio mollitia debitis
    accusamus neque molestiae laudantium delectus doloremque aliquam atque consequatur! Harum repellendus tenetur in
    nemo, voluptas autem est dicta laboriosam, id sed repudiandae deserunt quam tempora? Voluptates fugiat at
    reprehenderit vero earum, suscipit dicta porro. Corporis eaque cupiditate error praesentium molestiae atque earum
    iste aliquid incidunt, fugit perspiciatis? Nam eligendi ad laudantium magni accusamus repudiandae, molestias
    nesciunt necessitatibus amet aliquid, illo delectus. Harum fugiat repellat culpa, dicta voluptates alias. Dolores
    vitae libero harum voluptates fugiat nobis saepe aut cupiditate repellat placeat, veniam ullam dicta. Rem deleniti
    impedit blanditiis nemo, quos magni incidunt, ducimus similique ex officia id iste omnis sit esse. Earum veritatis
    magnam eum voluptas suscipit voluptate ratione quod ducimus autem aliquid? Ratione temporibus recusandae debitis
    veritatis repellendus doloribus libero saepe! Ipsam eligendi nam corporis illum consequuntur. Repellendus officia,
    blanditiis reprehenderit excepturi perferendis rerum et, id ex modi nostrum reiciendis ducimus est perspiciatis
    iusto minus, in cumque animi mollitia nihil iste praesentium aut incidunt! Dicta distinctio consequatur eaque!
    Similique quidem velit corrupti tempore numquam facere iusto ratione, explicabo fugiat accusamus asperiores adipisci
    optio officia illo earum? Nihil, sapiente culpa corrupti animi magnam quaerat natus laudantium impedit dicta
    provident, asperiores beatae sed neque labore enim similique est sint mollitia molestias optio commodi cupiditate,
    magni iste quibusdam. Sed nihil velit iusto voluptatum! Deleniti suscipit minima pariatur itaque molestiae adipisci
    neque harum incidunt doloribus enim unde, impedit aspernatur provident ullam at nam. Error molestias, eligendi omnis
    blanditiis numquam, repellendus nostrum placeat, autem ipsa sequi itaque pariatur doloribus minus esse fugit sint?
    Sunt laudantium molestiae debitis, eveniet, sint numquam quod cum nulla explicabo magnam exercitationem beatae magni
    ab optio. Asperiores commodi eos officia perspiciatis ipsum incidunt modi, exercitationem eveniet vel nam culpa
    animi omnis cum eius nemo quod illum labore harum repudiandae voluptas. Dolorum voluptas qui, magni quisquam
    architecto tenetur, repellendus earum perspiciatis rem ratione eveniet amet laboriosam distinctio facilis placeat,
    officia laborum voluptatem? Provident distinctio temporibus impedit fuga sequi cum? Quod rerum quaerat atque officia
    nesciunt in nulla dolores ipsum harum unde repudiandae repellat amet, nostrum dicta iusto sed voluptate assumenda
    error. Laboriosam iusto facilis beatae tempore numquam assumenda corporis reiciendis iste a magni. Non praesentium
    rem tenetur magni hic qui placeat nostrum quo nesciunt! Iure, saepe odit error accusantium veniam numquam. Est,
    laudantium! Impedit facilis delectus sit facere laboriosam saepe ducimus quo, ab debitis, minus obcaecati sapiente,
    hic harum dolores. Fugit omnis quis fuga eius! Illum cumque deserunt, eaque tempora aut porro perferendis iure
    voluptates est maiores numquam iste quo ut excepturi eos et assumenda officia nisi vel voluptas odit. Exercitationem
    ipsum soluta provident fugiat minus sapiente suscipit sed minima voluptates, reiciendis dignissimos doloribus
    impedit saepe dolorem sunt obcaecati pariatur magni laborum facere molestias odit neque. Facilis repellat quos unde
    modi architecto quasi non quibusdam dolor, alias libero, necessitatibus voluptas laudantium nisi recusandae ullam
    voluptatum. Quod non, adipisci porro sapiente perferendis culpa suscipit nesciunt a harum laborum fugiat quae minima
    at praesentium dolorem esse. Deleniti enim consequuntur, ipsa, impedit vero nam soluta accusamus laboriosam ducimus
    alias itaque optio illum voluptate iste voluptas illo expedita culpa! Porro incidunt commodi sapiente natus
    molestiae suscipit nisi. Voluptates ab aliquam doloribus. Ut quos ullam, voluptates pariatur totam nulla reiciendis
    ducimus. Incidunt fugiat reiciendis rem laborum quia illum. Quas, autem dolorum earum incidunt maiores, recusandae
    iusto quasi tenetur nemo nesciunt vero officiis, quibusdam aliquid minus animi nostrum a veritatis deleniti illum
    quis? Nihil eaque eum, error quidem facere voluptas at fuga modi debitis quisquam ipsam maiores aut provident
    aliquam deleniti repellendus harum! Laboriosam voluptate aut harum cum eum nulla, vero quasi veniam. Officiis amet
    nisi sit. Odit rerum quaerat repellendus molestias eum optio, soluta dolores explicabo dignissimos sed. Numquam
    provident deleniti vero qui. Similique aliquid consectetur doloremque! Similique aut, molestias ex ipsum id soluta
    provident sapiente! Adipisci repudiandae vitae consequuntur nulla dignissimos sed dolor et, minima hic explicabo
    assumenda culpa repellat quia? Porro corrupti corporis nam optio voluptate, labore pariatur, fugiat tenetur fuga
    veniam aliquid harum iste, ad cupiditate facere tempore numquam officia laboriosam expedita sunt ullam distinctio
    odit quasi. Consequuntur placeat eligendi tempora odit. Pariatur enim eaque assumenda placeat ipsa mollitia
    inventore exercitationem dolore, accusamus consequatur, quasi incidunt vero nihil officiis dolorum id, eligendi
    nobis vitae. Fugiat provident voluptatem quibusdam atque ipsa obcaecati dolor labore recusandae! Sit voluptatem
    porro eaque eveniet illo commodi fuga quia quaerat aspernatur, ipsam cumque explicabo tempore cum dicta dolores
    enim, blanditiis est delectus ducimus odit. Odit facere, tempore itaque reprehenderit, dolor quaerat libero rem
    accusantium, ut fugit ducimus fuga assumenda? Dolorum, odio tempora magnam laborum quos repellat asperiores
    explicabo velit, iste ex ad, architecto porro nulla nemo nobis neque nisi rem quia reprehenderit autem. Amet error
    delectus dicta ipsa pariatur veritatis ducimus aut alias qui non, explicabo accusantium nostrum itaque provident
    obcaecati, sed earum distinctio cum animi consequuntur commodi. Vitae eos culpa tenetur. Corporis obcaecati
    voluptates mollitia, recusandae nobis necessitatibus nesciunt voluptatem, nihil cum laborum iusto! Doloremque sequi
    praesentium dicta minus iusto saepe dolor ullam, porro atque possimus? Molestias eligendi, aspernatur ipsam,
    perspiciatis dolore doloribus eos, eveniet aperiam numquam asperiores delectus itaque praesentium veniam enim nam
    corporis harum aliquam excepturi minus qui ipsum accusamus animi? Saepe, deserunt? Quibusdam, reprehenderit nobis
    recusandae ipsum doloremque, molestias aut delectus minima nulla, animi consequatur accusantium quasi autem quia
    quos hic ad laborum blanditiis corporis! Blanditiis asperiores illum sapiente perspiciatis enim tenetur, officiis
    quos deserunt accusamus vero, dignissimos non, delectus doloribus!
  </div>
</template>
