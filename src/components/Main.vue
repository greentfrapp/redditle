<template>
  <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col gap-4 items-center">
    <h1 class="font-medium text-5xl sm:text-6xl font-title">
      <span class="text-red-500">reddit</span>le
    </h1>
    <div class="relative block max-w-screen px-4 sm:px-0 w-[35rem] text-gray-800">
      <div class="absolute inset-y-0 left-0 pl-8 sm:pl-4 flex items-center">
        <SearchIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </div>
      <input autofocus v-model="query" type="text" name="query" @keyup.enter="submit"
        placeholder="Try prefixing with r/<subreddit> for a specific subreddit"
        class="block w-full border border-gray-300 rounded-full py-3 pl-12 hover:shadow-catche focus:shadow-around focus:ring-0 focus:border-white focus-visible:outline-none" />
    </div>
    <div class="flex flex-col gap-2">
      <button class="text-gray-800 bg-gray-100 px-4 py-2 rounded hover:shadow-around border border-gray-300" @click="submit">Search</button>
      <a class="w-max text-red-500 text-sm" href="https://www.producthunt.com/posts/redditle" target="_blank">(Psst we're on ProductHunt!)</a>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { SearchIcon } from '@heroicons/vue/outline'

export default defineComponent({
  components: {
    SearchIcon,
  },
  data () {
    return {
      query: '',
    }
  },
  methods: {
    submit () {
      if (this.query) window.location.href = `/search?q=${encodeURIComponent(this.query)}`
    }
  }
})
</script>