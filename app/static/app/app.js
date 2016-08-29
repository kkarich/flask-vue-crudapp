var vm = new Vue({

  // We want to target the div with an id of 'events'
  el: '#app',

  // Here we can register any values or collections that hold data
  // for the application
  data: {
    people:[],
    newPerson:{ firstName:'', lastName:'', dateOfBirth:'',zipCode:'', loading:false }
  },

  // Anything within the ready function will run when the application loads
  ready: function() {
    this.getPeople();
  },

  // Methods we want to use in our application are registered here
  methods: {
    getPeople:function(){
        // GET /someUrl
        this.$http.get('/api/person').then((response) => {
            // success callback
          this.people = response.data;
        }, (response) => {
            // error callback
        });
    },
    addPerson:function(){
        this.newPerson.loading = true;
        var person = this.newPerson;
        // GET /someUrl
        this.$http.post('/api/person', person).then((response) => {
            // success callback
            var newPerson = JSON.parse(response.body);

            this.newPerson.loading = false;
            // Clear out new person form



            // add new person to start of list
            this.people.unshift(newPerson);
        }, (response) => {
          console.log(response)
            // error callback
          debugger;
            this.newPerson.loading = false;
        });

    },
    updatePerson:function(index){

    },
    deletePerson:function(index){
        var person = this.people[index];
        // GET /someUrl
        this.$http.delete('/api/person/'+person.id).then((response) => {
            // success callback
          this.people.splice(index,1);
        }, (response) => {
            // error callback
        });
    }
  }
});
