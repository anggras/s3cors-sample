<script>

export default {
  props: ['title', 'endpoint'],
  data() {
      return {
        presignedUrl: null,
        files: null,
        uploadDisabled: true,
      }
  },
  methods: {
    selectFile(event) {
      const fileName = event.target.files[0].name;
      const params = new URLSearchParams({
        path: "uploads/" + fileName
      });

      fetch(this.endpoint + "/url?" + params.toString())
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.presignedUrl = data;
          this.uploadDisabled = false;
          this.files = event.target.files;
        });
    },
    submitFile() {
      let formData = new FormData();

      let fields = this.presignedUrl.fields;
      for (const key in fields) {
        if (Object.hasOwnProperty.call(fields, key)) {
          formData.append(key, fields[key]);
        }
      }
      formData.append('file', this.files[0]);

      fetch(this.presignedUrl.url, {
        method: 'POST',
        headers: {
          "X-Custom-Header": "helloworld"
        },
        body: formData
      } )
      .then(response => {
        console.log(response);
      });
    }
  }
}
</script>

<template>
  <fieldset >
    {{title}}
    <div>
      <input type="file" @change="selectFile" ref="file" name="file">
      <button @click="submitFile" :disabled="uploadDisabled">Upload</button>
    </div>
  </fieldset>
</template>