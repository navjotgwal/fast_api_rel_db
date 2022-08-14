window.onload = function(){
    form = document.getElementById("updateForm");
    delete_btn = document.getElementById("deletemovie");
    console.log(form)
    function updateMovie(id, name, desc) {
      res = fetch("/movie/" + id, {
        method: "PATCH",
        body: JSON.stringify({
          name,
          desc,
        }),
      }).then((response) => response.json());
      window.location.reload();
    }

    async function deleteMovie(id) {
      const res = await fetch("/movie/" + id, {
        method: "DELETE",
      }).then((response) => response.json());
      window.location.reload();
    }
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const des = document.getElementById("desc").value;
      const id = document.getElementById("id").value;
      updateMovie(id, name, des);
    });
    delete_btn.addEventListener("click", (e) =>{
        const id = document.getElementById("id").value;
        deleteMovie(id);
    });
  };