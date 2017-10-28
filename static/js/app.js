var app = new Vue({
  el: '#app',
  data: {
    activeIndex: '1',
    total: 0,
    page_size: 20,
    tableData: [],
    apiUrl: 'http://localhost:8000/api/proxy?',
    args: {
      https: null,
      anonymous: null,
      page: 1,
      page_size: null,
    }
  },
  mounted: function() {
    this.getProxies({});
  },
  methods: {
    getProxies: function(args){

      if (args.https != undefined) {
        this.args.https = args.https
      }
      if (args.anonymous != undefined) {
        this.args.anonymous = args.anonymous;
      }
      if (typeof(args.page) == 'number') {
        this.args.page = args.page;
      }

      var url = this.apiUrl

      if (this.args.https != null) {
        url += '&https=' + this.args.https;
      }
      if (this.args.anonymous != null) {
        url += '&anonymous=' + this.args.anonymous;
      }
      url += '&page=' + this.args.page;

      this.$http.get(url).then(response => {
        this.tableData = response.data.proxies;
        this.total = response.data.total;
      })
    },
    handleCurrentChange: function(val) {
      this.getProxies({page: val});
    }
  }
})