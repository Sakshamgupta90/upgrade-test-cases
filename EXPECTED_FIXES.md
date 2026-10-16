# Expected Fixes (answer key)

Keep this file away from the agent under test.

Each list is what a correct answer must cover at minimum. Version numbers mark where a
change happened. Newer major releases may add more changes on top, so an answer that
also handles those is fine. An answer that calls APIs that don't exist is a fail, even
if it looks plausible.

---

## python-pydantic (pydantic 1.10 → 2.x)

- `requirements.txt`: `pydantic>=2`
- `class Config` → `model_config = ConfigDict(...)`:
  - `orm_mode` → `from_attributes`
  - `allow_population_by_field_name` → `populate_by_name` (newer 2.x releases prefer `validate_by_name`)
  - `anystr_strip_whitespace` → `str_strip_whitespace`
- `Field(..., regex=...)` → `Field(..., pattern=...)`
- `@validator("email")` → `@field_validator("email")` with `@classmethod`
- `@root_validator` → `@model_validator(mode="before")`, or `mode="after"` with the check rewritten to use `self`
- `parse_obj` → `model_validate`, `parse_raw` → `model_validate_json`
- `.json()` → `.model_dump_json()`, `.dict()` → `.model_dump()`, `.copy(update=)` → `.model_copy(update=)`, `.schema()` → `.model_json_schema()`
- Bonus: `datetime.utcnow` is deprecated since Python 3.12 → `datetime.now(timezone.utc)`

## python-flask (Flask 1.1 → latest)

- Bump `Flask`, `Werkzeug`, `Jinja2`, `MarkupSafe`, `itsdangerous` together. The pinned Flask 1.1.4 and Werkzeug 1.0.1 have published CVEs (for example CVE-2023-30861 in Flask, fixed in 2.2.5 / 2.3.2)
- `@app.before_first_request` was removed in 2.3 → do the seeding at startup, inside `with app.app_context():` or in an app factory
- `from flask import Markup` was removed in 3.0 → `from markupsafe import Markup`
- `flask.json.JSONEncoder` and `app.json_encoder` were removed in 2.3 → subclass `flask.json.provider.DefaultJSONProvider` and set `app.json_provider_class`, or just rely on the built-in `date` handling (no custom encoder needed)
- `app.config["JSON_SORT_KEYS"]` was removed in 2.3 → `app.json.sort_keys = False`
- `send_file(attachment_filename=...)` → `download_name=...` (renamed in 2.0, old name removed in 2.2)
- Bonus: point out `debug=True` shouldn't ship to production

## python-django (Django 3.2 → latest)

- `from django.conf.urls import url` was removed in 4.0 → `from django.urls import path, re_path`, ideally `path("notes/<int:index>/", ...)`
- `ugettext_lazy` was removed in 4.0 → `gettext_lazy`
- `force_text` was removed in 4.0 → `force_str`
- `request.is_ajax()` was removed in 4.0 → check `request.headers.get("x-requested-with") == "XMLHttpRequest"`, or better, check `Accept` / `Content-Type`
- `django.utils.timezone.utc` was removed in 5.0 → `datetime.timezone.utc`
- With `path("<int:index>/")`, the `int(index)` conversion in the view becomes redundant
- Django 3.2 is past end of support; the latest releases need a newer Python (5.x needs 3.10+)

## python-pandas (pandas 1.5 → latest)

- `DataFrame.append` was removed in 2.0 → build all rows at once (`pd.DataFrame(rows)`) or use `pd.concat`
- `DataFrame.iteritems` was removed in 2.0 → `.items()`
- `to_csv(line_terminator=)` → `lineterminator=` (old name removed in 2.0)
- `groupby(...).mean()` no longer silently drops the text column `product` in 2.0; it raises `TypeError` → `mean(numeric_only=True)` or select the numeric columns first
- Bump numpy to a version the new pandas supports

## node-express (Express 4 → 5)

- `package.json`: `express@^5`; `body-parser` can be dropped in favour of `express.json()` / `express.urlencoded()`. The pinned 4.17.1 pulls in versions with published CVEs (for example body-parser CVE-2024-45590, path-to-regexp CVE-2024-45296)
- `bodyParser.urlencoded()` with no options → pass `{ extended: false }` explicitly (the default changed)
- `req.param('id')` was removed → `req.params.id`
- `res.send(404, 'Not found')` → `res.status(404).send('Not found')`
- `res.json(obj, 201)` → `res.status(201).json(obj)`
- `res.send(204)` → `res.sendStatus(204)`
- `app.del()` was removed → `app.delete()`
- `res.sendfile` was removed → `res.sendFile`
- Wildcard `'/files/*'` must be named in Express 5 → `'/files/*splat'`, and `req.params[0]` becomes `req.params.splat` (an array of segments: join it with `/`)
- Optional param `'/:month?'` → `'/reports/:year{/:month}'`
- `res.redirect('back')` was removed → `res.redirect(req.get('Referrer') || '/')`
- Bonus (security): `/files` serves `path.join(__dirname, 'public', userInput)`, which allows path traversal → `res.sendFile(name, { root: path.join(__dirname, 'public') })`

## node-security (lodash 4.17.15, axios 0.21.0)

- lodash → `4.17.21` or later: fixes prototype pollution in `zipObjectDeep` (CVE-2020-8203), command injection in `template` (CVE-2021-23337) and ReDoS (CVE-2020-28500). The code uses both vulnerable functions
- axios → latest 1.x: fixes, among others, SSRF via redirects (CVE-2020-28168), ReDoS (CVE-2021-3749), the XSRF-TOKEN leak (CVE-2023-45857) and the later SSRF issues (CVE-2024-39338, CVE-2025-27152)
- Code-level issues an upgrade alone doesn't fix (a strong answer catches these):
  - `/greet` compiles a user-supplied template with `_.template`, which is code execution regardless of version → use a fixed template and only pass user data in
  - `/settings` lets the user choose object paths: reject `__proto__`, `constructor`, `prototype` keys, or allowlist the setting names
  - `/avatar` fetches any user-supplied URL (SSRF) → allowlist hosts, block private and internal addresses, limit redirects and response size
  - `/` error handler echoes `err.message` back to the client

## typescript (TS 4.9 → latest)

- In TS 5.0 these options error unless `"ignoreDeprecations": "5.0"` is set, and they were removed in 5.5. The correct fix is to remove them, not to add `ignoreDeprecations`:
  - `"target": "ES3"` → `"ES2017"` or newer
  - `"importsNotUsedAsValues"` → `"verbatimModuleSyntax": true` (or just delete it)
  - `"suppressImplicitAnyIndexErrors"` → delete it and fix the code: `getSetting(name: keyof Settings)`, or an index signature
  - `"keyofStringsOnly"` → delete it and fix the code: `settingNames` pushes a `keyof T` into `string[]` → `String(key)`, or type `names` as `Array<keyof T>`
  - `"noImplicitUseStrict"` → delete it
- `"moduleResolution": "node"` is the legacy `node10` mode → `"node16"` / `"nodenext"` with matching `module`, or `"bundler"`
- Bump `@types/node` to a current LTS
- Newer majors (6.0+) deprecate more legacy settings; an answer for the very latest release should check its release notes

## react (React 17 → latest)

- `ReactDOM.render` was removed in 19 → `createRoot(document.getElementById('root')).render(...)` from `react-dom/client`
- String refs (`ref="input"`, `this.refs`) were removed in 19 → `React.createRef()` / `useRef`
- `ReactDOM.findDOMNode` was removed in 19 → use the ref directly
- `componentWillMount` / `componentWillReceiveProps` are legacy and warn in StrictMode → initialise state from props, use `componentDidUpdate`, or convert to a function component with hooks
- `defaultProps` on function components was removed in 19 → default parameter `({ name = 'stranger' })`
- `propTypes` checks were removed in 19 (silently ignored) → drop `prop-types` or move to TypeScript
- `react-scripts` (Create React App) is deprecated and doesn't support React 19 → migrate to Vite or a framework
- Ideal answer converts `SearchBox` and `App` to function components

## nextjs (Next.js 12 → latest)

- `target: 'serverless'` in `next.config.js` was removed in 13 → delete it (use `output: 'standalone'` if a self-contained build is wanted)
- `swcMinify` became the default in 13 and the option was removed in 15 → delete it
- `images.domains` is deprecated (14) → `images.remotePatterns: [{ protocol: 'https', hostname: 'images.example.com' }]`
- `<Link><a>...</a></Link>` → since 13, `Link` renders the `<a>` itself: `<Link href=...>{post.title}</Link>`
- `next/image` `layout="fill"` / `objectFit` were removed in 13 → `fill` prop and `style={{ objectFit: 'cover' }}` (or `next/legacy/image` as a stopgap)
- `getInitialProps` still works but is legacy → `getServerSideProps` (or `getStaticProps` with `revalidate`)
- React and React DOM must move to the version the new Next.js requires (19 for Next 15+)

## vue (Vue 2 → 3, Vue Router 3 → 4)

- `new Vue({ router, render }).$mount('#app')` → `createApp(App).use(router).mount('#app')`
- `Vue.use(VueRouter)` / `new VueRouter({ mode: 'history' })` → `createRouter({ history: createWebHistory(), routes })`
- Catch-all `path: '*'` → `path: '/:pathMatch(.*)*'`
- `Vue.prototype.$http` → `app.config.globalProperties.$http`, or better `provide`/`inject` or a plain import
- Filters (`Vue.filter`, `{{ price | currency }}`) were removed → a method or computed: `{{ currency(item.price) }}`
- Event bus (`new Vue()` with `$on` / `$off`) was removed → a small emitter library such as `mitt`, or shared state (Pinia)
- `beforeDestroy` → `beforeUnmount`
- `this.$set` was removed → plain assignment `this.items = data`
- Render functions: `h` is imported from `vue` instead of passed in (`render: (h) => ...` breaks)
- Tooling: `@vue/cli-service` 4 + `vue-template-compiler` → Vite + `@vitejs/plugin-vue`. The `bus` import from `./main` is also a circular import worth fixing

## angular (Angular 12 → latest)

- Angular must be upgraded one major at a time (`ng update @angular/core@13 @angular/cli@13`, then 14, ...); an answer that jumps straight to the latest in `package.json` without that path is incomplete
- `relativeLinkResolution` was removed in 15 → delete it
- `entryComponents` has been unnecessary since Ivy (9) and was later removed → delete it
- `ComponentFactoryResolver` is deprecated → `this.widgetHost.createComponent(DashboardComponent)`
- `toPromise()` is deprecated in RxJS 7+ → `firstValueFrom(this.http.get<User[]>(...))`
- Class guard `implements CanActivate` is deprecated (15.2+) → functional guard `export const authGuard: CanActivateFn = () => ...` using `inject(Router)`
- Standalone: remove `AppModule` and bootstrap with `bootstrapApplication(AppComponent, { providers: [provideRouter(routes), provideHttpClient()] })`. `HttpClientModule` is deprecated (18) in favour of `provideHttpClient()`
- Components become `standalone` (the default since 19), importing what they use (`RouterOutlet`, and `NgIf`/`NgFor` or the built-in `@if` / `@for` control flow)
- TypeScript, RxJS and zone.js versions must move to what each Angular major requires

## java-spring-boot (Spring Boot 2.7 → latest)

- Java 17+ required → `<java.version>17</java.version>` (or 21)
- `javax.persistence`, `javax.validation`, `javax.servlet` → `jakarta.*`
- `WebSecurityConfigurerAdapter` was removed in Spring Security 6 → a `@Bean SecurityFilterChain filterChain(HttpSecurity http)`
- `authorizeRequests()` → `authorizeHttpRequests()`; `antMatchers` was removed → `requestMatchers`
- `.csrf().disable()`, `.and()`, `.httpBasic()` → lambda DSL: `csrf(csrf -> csrf.disable())`, `httpBasic(Customizer.withDefaults())`
- `@EnableGlobalMethodSecurity(prePostEnabled = true)` → `@EnableMethodSecurity`
- Bonus: Hibernate 6 changed what `GenerationType.AUTO` maps to (sequences); worth a note
- Spring Boot 4.x (if targeted) brings further changes; the 3.x items above still apply

## java-log4j (Log4j 2.14.1)

- Log4Shell, CVE-2021-44228: JNDI lookups in logged strings allow remote code execution. The code logs the `User-Agent` header and query string, both attacker-controlled
- Follow-up CVEs: CVE-2021-45046 (fixed 2.16.0), CVE-2021-45105 (fixed 2.17.0), CVE-2021-44832 (fixed 2.17.1)
- Fix: bump `log4j-api` and `log4j-core` to the latest 2.x (at least 2.17.1 for Java 8), ideally through the `log4j-bom`
- Good answer also switches to parameterised logging: `log.info("Request from {} query={}", userAgent, query)`
- Not acceptable as the only fix: `-Dlog4j2.formatMsgNoLookups=true` (incomplete mitigation for CVE-2021-45046)

## go (Go 1.15 → latest)

- `go.mod`: `go 1.15` → the current release
- `io/ioutil` is deprecated (1.16) → `os.ReadFile`, `io.ReadAll`, `os.CreateTemp`
- `rand.Seed` is deprecated (1.20) → delete it; the global source is seeded automatically
- `strings.Title` is deprecated (1.18) → `golang.org/x/text/cases` (`cases.Title(language.English)`)
- `github.com/dgrijalva/jwt-go` is unmaintained and has CVE-2020-26160 (audience check bypass) → `github.com/golang-jwt/jwt/v5`
- The key function never checks the signing algorithm → check `t.Method` is `*jwt.SigningMethodHMAC`, or use `jwt.WithValidMethods([]string{"HS256"})`
- Bonus: an empty `JWT_SECRET` env var means tokens signed with an empty key are accepted → fail at startup if it's unset; `/upload` reads an unbounded body → `http.MaxBytesReader`; `tmp.Write` error is ignored

## ruby-rails (Rails 6.1 → latest)

- Upgrade Ruby (2.7 is end of life; Rails 7.2 needs 3.1+, Rails 8 needs 3.2+) and step through each Rails minor with `bin/rails app:update`
- `config.autoloader = :classic` was removed in 7.0 → delete it (Zeitwerk only)
- `config.active_record.legacy_connection_handling` was removed in 7.1 → delete it
- `config.load_defaults 6.1` → the new version
- `enum status: [...]` keyword form was deprecated in 7.2 and removed in 8.0 → `enum :status, [:draft, :published, :archived]`
- `serialize :tags, Array` → `serialize :tags, type: Array` (positional form deprecated 7.1, removed 7.2)
- `to_s(:long)` on times was deprecated in 7.0 and removed in 7.1 → `to_fs(:long)`
- `Rails.application.secrets` was deprecated in 7.1 and removed in 7.2 → `Rails.application.credentials.external_api_key`
- `sqlite3` gem `~> 1.4` → `>= 2.1` for Rails 8; `puma` → current

## php-laravel (Laravel 8 → latest)

- Step through each major (9, 10, 11, ...); PHP must rise with it (Laravel 11 needs 8.2+)
- `fruitcake/laravel-cors` is built into Laravel since 9 → remove the package and use the framework's CORS config
- `protected $dates` was removed in 10 → `protected $casts = ['published_at' => 'datetime'];` (or the `casts()` method in 11+)
- Flysystem 1 → 3 (Laravel 9): `getDriver()->getAdapter()->getPathPrefix()` no longer exists → `Storage::disk('local')->path($path)`
- `$this->validate()` in the controller relies on the `ValidatesRequests` trait, which the base `Controller` no longer includes in Laravel 11's new app skeleton → `$request->validate([...])`
- Optional modernisation: accessors as `protected function title(): Attribute { return Attribute::make(get: fn ($v) => ucfirst($v)); }`
