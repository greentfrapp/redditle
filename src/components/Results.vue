<template>
  <!-- Top -->
  <div class="flex flex-col sm:flex-row items-center py-4 sm:py-6 border border-white gap-2 sm:gap-0 fixed bg-white top-0 w-full text-gray-800"
    :class="isAtTop ? 'border-b-2 border-gray-100' : 'shadow-md'">
    <a href="/" class="font-medium text-2xl font-title mx-2 sm:mx-8">
      <span class="text-red-500">reddit</span>le
    </a>
    <div class="relative block max-w-screen px-4 sm:px-0 w-[35rem]">
      <input autofocus v-model="query" type="text" name="query" @keyup.enter="submit"
        class="block w-full border border-gray-300 rounded-full py-2 sm:py-3 pl-8 hover:shadow-around focus:shadow-around focus:ring-0 focus:border-0 focus-visible:outline-none" />
      <div class="absolute inset-y-0 right-0 pr-8 sm:pr-4 items-center flex">
        <XIcon class="h-5 w-5 text-gray-400 border-gray-200 cursor-pointer" @click="clear" aria-hidden="true" :class="loading ? 'animate-spin' : ''" />
        <div class="h-3/5 w-0.5 bg-gray-100 mx-2"></div>
        <SearchIcon class="h-5 w-5 text-light-blue cursor-pointer" @click="submit" aria-hidden="true" />
      </div>
    </div>
  </div>
  <!-- Results -->
  <div class="max-w-screen sm:max-w-2xl px-4 sm:px-0 sm:ml-48 mt-36 sm:mt-32 text-gray-800">
    <div v-if="loading" class="my-4 text-sm">
      Loading...
    </div>
    <div v-else-if="results.length">
      <div class="my-4 text-sm">{{stats}}</div>
      <div class="flex flex-col gap-8">
        <div v-for="(result, i) in results" :key="i">
          <a :href="result.href" class="text-link-blue text-xl">{{ result.title }}</a>
          <p>{{ result.desc }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="my-4 text-sm">No results found :(</div>
    </div>
  </div>
  <!-- Footer -->
  <div v-if="numPages > 1" class="max-w-screen sm:max-w-2xl px-4 sm:px-0 sm:ml-48 mt-20 mb-36 text-gray-800">
    <h1 class="font-medium text-3xl font-title mx-8 flex w-max mx-auto">
      <!-- Prev -->
      <div v-if="currentPage !== 1" class="inline px-0 mx-0 flex flex-col w-max items-center mx-2 cursor-pointer" @click="paginate(currentPage-1)">
        <div class="flex items-center">
          &nbsp;
          <ChevronLeftIcon class="h-5 w-5 cursor-pointer" @click="search" aria-hidden="true" />
          &nbsp;
        </div>
        <div class="text-sm text-light-blue font-sans">Prev</div>
      </div>
      <span class="text-red-500">re</span>
      <div v-for="p in numPages" :key="p" class="inline px-0 mx-0 flex flex-col w-max items-center"
        :class="currentPage === p + paginateStart ? '' : 'cursor-pointer text-red-500'" @click="paginate(p + paginateStart)">
        d
        <div class="text-sm font-sans" :class="currentPage === p + paginateStart ? '' : 'text-light-blue'">
          {{ p + paginateStart }}
        </div>
      </div>
      <span class="text-red-500">it</span>le
      <!-- Next -->
      <div v-if="currentPage !== numPages" class="inline px-0 mx-0 flex flex-col w-max items-center mx-2 cursor-pointer" @click="paginate(currentPage+1)">
        <div class="flex items-center">
          &nbsp;
          <ChevronRightIcon class="h-5 w-5 cursor-pointer" @click="search" aria-hidden="true" />
          &nbsp;
        </div>
        <div class="text-sm text-light-blue font-sans">Next</div>
      </div>
    </h1>
  </div>
  <div v-else class="h-36" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { XIcon, SearchIcon, ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/outline'

interface Result {
  title: string;
  href: string;
  desc: string;
}

export default defineComponent({
  mounted () {
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
      const paginateEnd = Math.max(Math.min(this.currentPage + 4, (this.numResults / 10)), 10)
      return paginateEnd - 10
    },
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
        if (results.stats) {
          this.stats = results.stats
          this.results = results.results
          // Regex to extract number of results
          const numResultsStr = results.stats.match(/\d+(,?\d+)* results/)
          if (numResultsStr) {
            this.numResults = parseInt(numResultsStr[0].replaceAll(',', ''))
          } else {
            this.numResults = 0
          }
        } else {
          this.results = []
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