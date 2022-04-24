<template>
  <div class="min-h-screen" :class="[darkMode ? 'bg-neutral-800 text-neutral-300' : 'bg-white text-neutral-900']">
    <div class="fixed z-50 w-full">
      <div class="flex gap-1 items-center justify-end p-2">
        <SunIcon class="h-5" :class="[darkMode ? 'text-neutral-600' : 'text-neutral-300']" />
        <Switch v-model="darkMode" :class="[darkMode ? 'bg-neutral-600' : 'bg-neutral-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-0']">
          <span class="sr-only">Use setting</span>
          <span aria-hidden="true" :class="[darkMode ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
        </Switch>
        <MoonIcon class="h-5" :class="[darkMode ? 'text-neutral-600' : 'text-neutral-300']" />
      </div>
    </div>
  <!-- Top -->
  <div class="flex flex-col sm:flex-row items-center justify-between pt-10 pb-4 sm:py-6 gap-2 sm:gap-0 fixed top-0 w-full"
    :class="[darkMode ? 'bg-neutral-800 text-neutral-300' : 'bg-white text-neutral-900', darkMode ? (isAtTop ? 'border-b-2 border-neutral-700' : 'shadow-md') : (isAtTop ? 'border-b-2 border-neutral-100' : 'shadow-md')]">
    <div class="flex flex-col sm:flex-row items-center">
      <a href="/" class="font-medium text-2xl font-title mx-2 sm:mx-8">
        <span :class="darkMode ? 'text-red-400' : 'text-red-500'">reddit</span>le
      </a>
      <div class="relative block max-w-screen px-4 sm:px-0 w-[35rem]">
        <input autofocus v-model="query" type="text" name="query" @keyup.enter="submit"
          class="block w-full border rounded-full py-2 sm:py-3 pl-8 hover:shadow-around focus:shadow-around focus:ring-0 focus-visible:outline-none bg-transparent" :class="darkMode ? ' focus:border-neutral-600 border-neutral-600' : 'focus:border-0 border-neutral-300'" />
        <div class="absolute inset-y-0 right-0 pr-8 sm:pr-4 items-center flex">
          <XIcon class="h-5 w-5 text-neutral-400 border-neutral-200 cursor-pointer" @click="clear" aria-hidden="true" :class="loading ? 'animate-spin' : ''" />
          <div class="h-3/5 w-0.5 mx-2" :class="darkMode ? 'bg-neutral-600' : 'bg-neutral-200'"></div>
          <SearchIcon class="h-5 w-5 cursor-pointer" @click="submit" aria-hidden="true" :class="darkMode ? 'text-dark-blue' : 'text-light-blue'" />
        </div>
      </div>
      <div class="px-4 py-1 flex gap-2 items-center">
        <input class="cursor-pointer rounded bg-transparent focus:ring-0" :class="darkMode ? 'checked:bg-red-400 focus:checked:bg-red-400 hover:checked:bg-red-400' : 'checked:bg-red-500 focus:checked:bg-red-500 hover:checked:bg-red-500'" type="checkbox" id="oldreddit" v-model="useOldReddit" />
        <label class="cursor-pointer" for="oldreddit">Use old.reddit.com</label>
      </div>
    </div>
  </div>
  <!-- Results -->
  <div class="max-w-screen sm:max-w-2xl px-4 sm:px-0 sm:ml-48 pt-44 sm:pt-32" :class="darkMode ? 'text-neutral-300' : 'text-neutral-800'">
    <div v-if="loading" class="my-4 text-sm">
      Loading...
    </div>
    <div v-else-if="results.length">
      <div class="my-4 text-sm">{{stats}}</div>
      <div class="flex flex-col gap-8">
        <div v-for="(result, i) in results" :key="i">
          <a :href="useOldReddit ? result.href.replace('www.reddit.com', 'old.reddit.com') : result.href" class="text-xl" :class="darkMode ? 'text-dark-blue' : 'text-link-blue'">{{ result.title }}</a>
          <p>{{ result.desc }}</p>
        </div>
      </div>
    </div>
    <div v-else-if="error">
      <div class="my-4 text-sm">{{error}}</div>
    </div>
    <div v-else>
      <div class="my-4 text-sm">No results found :(</div>
    </div>
  </div>
  <!-- Footer -->
  <div class="max-w-screen sm:max-w-2xl px-4 sm:px-0 sm:ml-48 mt-20 pb-36 text-neutral-800">
    <h1 class="font-medium text-3xl font-title mx-8 flex w-max mx-auto">
      <!-- Prev -->
      <div v-if="hasPrev" class="inline px-0 mx-0 flex flex-col w-max items-center mx-2 cursor-pointer" @click="paginate(currentPage-1)">
        <div class="flex items-center">
          &nbsp;
          <ChevronLeftIcon class="h-5 w-5 cursor-pointer" aria-hidden="true" :class="darkMode ? 'text-gray-300' : ''" />
          &nbsp;
        </div>
        <div class="text-sm font-sans" :class="darkMode ? 'text-dark-blue' : 'text-light-blue'">Prev</div>
      </div>
      <span :class="darkMode ? 'text-red-400' : 'text-red-500'">re</span>
      <div v-for="p in Math.min(currentPage, 9)" :key="p" class="inline px-0 mx-0 flex flex-col w-max items-center"
        :class="currentPage === p + paginateStart ? (darkMode ? 'text-neutral-300' : '') : (darkMode ? 'cursor-pointer text-red-400' : 'cursor-pointer text-red-500')" @click="paginate(p + paginateStart)">
        d
        <div class="text-sm font-sans" :class="currentPage === p + paginateStart ? '' : (darkMode ? 'text-dark-blue' : 'text-light-blue')">
          {{ p + paginateStart }}
        </div>
      </div>
      <div v-if="hasNext" class="inline px-0 mx-0 flex flex-col w-max items-center cursor-pointer" :class="darkMode ? 'text-red-400' : 'text-red-500'"
        @click="paginate(currentPage+1)">
        d
        <div class="text-sm font-sans" :class="darkMode ? 'text-dark-blue' : 'text-light-blue'">
          ...
        </div>
      </div>
      <div v-else class="inline px-0 mx-0 flex flex-col w-max items-center" :class="darkMode ? 'text-red-400' : 'text-red-500'">
        d
      </div>
      <span :class="darkMode ? 'text-red-400' : 'text-red-500'">it</span><span :class="[darkMode ? 'text-neutral-300' : 'text-neutral-900']">le</span>
      <!-- Next -->
      <div v-if="hasNext" class="inline px-0 mx-0 flex flex-col w-max items-center mx-2 cursor-pointer" @click="paginate(currentPage+1)">
        <div class="flex items-center">
          &nbsp;
          <ChevronRightIcon class="h-5 w-5 cursor-pointer" aria-hidden="true" :class="darkMode ? 'text-gray-300' : ''" />
          &nbsp;
        </div>
        <div class="text-sm font-sans" :class="darkMode ? 'text-dark-blue' : 'text-light-blue'">Next</div>
      </div>
    </h1>
  </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { XIcon, SearchIcon, ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/outline'
import { SunIcon, MoonIcon } from '@heroicons/vue/solid'
import { Switch } from '@headlessui/vue'

interface Result {
  title: string;
  href: string;
  desc: string;
}

export default defineComponent({
  mounted () {
    const useOldReddit = localStorage.getItem('useOldReddit')
    if (useOldReddit === 'true') this.useOldReddit = true
    const darkMode = localStorage.getItem('darkMode')
    if (darkMode === 'true') this.darkMode = true
    window.addEventListener("scroll", () => {
      this.isAtTop = window.scrollY === 0
    }, false)
    const url = new URL(window.location.href)
    this.query = decodeURIComponent(url.searchParams.get('q') || '')
    this.start = parseInt(url.searchParams.get('start') || '0') || 0
    this.search()
  },
  components: {
    XIcon,
    SearchIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    SunIcon,
    MoonIcon,
    Switch,
  },
  data () {
    return {
      isAtTop: true,
      loading: true,
      query: '',
      stats: '',
      results: [] as Result[],
      start: 0,
      numResults: 0,
      lambdaUrl: import.meta.env.VITE_LAMBDA as string,
      error: '',
      hasPrev: false,
      hasNext: false,
      useOldReddit: false,
      darkMode: false,
    }
  },
  computed: {
    numPages ():number {
      return Math.min(10, Math.ceil(this.numResults / 10))
    },
    currentPage ():number {
      return Math.ceil((this.start + 1) / 10)
    },
    paginateStart ():number {
      return Math.max(0, this.currentPage - 9)
    },
  },
  watch: {
    useOldReddit (useOldReddit) {
      if (useOldReddit) {
        localStorage.setItem('useOldReddit', 'true')
      } else {
        localStorage.setItem('useOldReddit', 'false')
      }
    },
    darkMode (darkMode) {
      if (darkMode) {
        localStorage.setItem('darkMode', 'true')
      } else {
        localStorage.setItem('darkMode', 'false')
      }
    }
  },
  methods: {
    submit () {
      window.location.href = encodeURI(`/search?q=${encodeURIComponent(this.query)}`)
    },
    clear () {
      this.query = ''
    },
    search () {
      fetch(this.lambdaUrl, {
        method: 'POST',
        body: JSON.stringify({
          query: this.query,
          start: this.start,
        })
      }).then(async response => {
        const results = await response.json()
        if (results.results) {
          this.results = results.results
          this.hasPrev = results.has_prev
          this.hasNext = results.has_next
        } else {
          this.results = []
          this.error = 'Sorry! We\'re getting overwhelmed at the moment!'
        }
      }).catch((error) => {
        console.error('Error:', error)
        this.results = []
      }).finally(() => {
        this.loading = false
      })
    },
    paginate (pageNum:number) {
      if (pageNum === 1) window.location.href = `/search?q=${encodeURIComponent(this.query)}`
      else window.location.href = encodeURI(`/search?q=${encodeURIComponent(this.query)}&start=${(pageNum-1)*10}`)
    },
  },
})
</script>