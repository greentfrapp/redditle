<template>
  <div class="h-screen w-screen" :class="[darkMode ? 'bg-neutral-800' : 'bg-white']">
    <div class="flex gap-1 items-center w-full justify-end p-2">
      <SunIcon class="h-5" :class="[darkMode ? 'text-neutral-600' : 'text-neutral-300']" />
      <Switch v-model="darkMode" :class="[darkMode ? 'bg-neutral-600' : 'bg-neutral-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-0']">
        <span class="sr-only">Use setting</span>
        <span aria-hidden="true" :class="[darkMode ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
      </Switch>
      <MoonIcon class="h-5" :class="[darkMode ? 'text-neutral-600' : 'text-neutral-300']" />
    </div>
    <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col gap-4 items-center">
      <h1 class="font-medium text-5xl sm:text-6xl font-title">
        <span :class="darkMode ? 'text-red-400' : 'text-red-500'">reddit</span><span :class="[darkMode ? 'text-neutral-100' : 'text-neutral-900']">le</span>
      </h1>
      <div class="relative block max-w-screen px-4 sm:px-0 w-[35rem]" :class="[darkMode ? 'text-neutral-200' : 'text-neutral-900']">
        <div class="absolute inset-y-0 left-0 pl-8 sm:pl-4 flex items-center">
          <SearchIcon class="h-5 w-5 text-neutral-400" aria-hidden="true" />
        </div>
        <input autofocus v-model="query" type="text" name="query" @keyup.enter="submit"
          placeholder="Try prefixing with r/<subreddit> for a specific subreddit"
          class="block w-full border rounded-full py-3 pl-12 hover:shadow-catche focus:shadow-around focus:ring-0 focus:border-white focus-visible:outline-none bg-transparent" :class="[darkMode ? 'border-neutral-700 placeholder:text-neutral-500' : 'border-neutral-300 placeholder:text-neutral-400']" />
      </div>
      <div class="flex flex-col gap-2">
        <button class=" px-4 py-2 rounded hover:shadow-around border"
          :class="[darkMode ? 'bg-neutral-800 text-neutral-300 border-neutral-700' : 'bg-neutral-100 text-neutral-800 border-neutral-300']"
          @click="submit">Search</button>
        <div>
          <a class="w-max text-sm" :class="darkMode ? 'text-red-300' : 'text-red-500'" href="https://github.com/sponsors/greentfrapp" target="_blank">Buy me a monthly coffee or </a>
          <a class="w-max text-sm" :class="darkMode ? 'text-red-300' : 'text-red-500'" href="https://twitter.com/sweekiat_lim" target="_blank">follow me on Twitter!</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { SearchIcon } from '@heroicons/vue/outline'
import { SunIcon, MoonIcon } from '@heroicons/vue/solid'
import { Switch } from '@headlessui/vue'

export default defineComponent({
  mounted () {
    const darkMode = localStorage.getItem('darkMode')
    if (darkMode === 'true') this.darkMode = true
  },
  components: {
    SearchIcon,
    SunIcon,
    MoonIcon,
    Switch,
  },
  data () {
    return {
      query: '',
      darkMode: false,
    }
  },
  watch: {
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
      if (this.query) window.location.href = `/search?q=${encodeURIComponent(this.query)}`
    }
  }
})
</script>