<template>
  <div id="app">
    <router-view />
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} - {{ item.price | currency }}
      </li>
    </ul>
    <button v-on:click="refresh">Refresh</button>
  </div>
</template>

<script>
import { bus } from './main';

export default {
  name: 'App',
  data() {
    return { items: [] };
  },
  created() {
    bus.$on('refresh', this.refresh);
    this.refresh();
  },
  beforeDestroy() {
    bus.$off('refresh', this.refresh);
  },
  methods: {
    async refresh() {
      const { data } = await this.$http.get('/api/items');
      this.$set(this, 'items', data);
    },
  },
};
</script>
