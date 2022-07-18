document.addEventListener("DOMContentLoaded", function (event) {
  const makeUiD = function () {
    return String(Date.now().toString(32) + Math.random().toString(16)).replace(
      /\./g,
      ""
    );
  };

  // Declare Container Variables
  var profileBgImageContainer = document.getElementById("profile_bg_image");
  var profileBgImgInput = document.getElementById("profile_bg_image_input");
  var profileBgImgChangeBtn = document.getElementById(
    "profile_bg_img_change_btn"
  );

  var bgImgModal = document.getElementById("background_img_modal");

  var bgImageModalContainer = bgImgModal
    ? new bootstrap.Modal(document.getElementById("background_img_modal"))
    : null;

  /**
   * Background Image Changing Process: Start
   *
   *
   */
  var bgImageList = document.querySelectorAll(".background_image_clicker");
  var selectedBgImgValue = null;

  // Check this page has bg Image List is getting
  if (bgImageList.length > 0) {
    // We need to make sure Add Click Listener
    bgImageList.forEach(function (bgClicker) {
      bgClicker.addEventListener("click", function () {
        var newBgClickerValue = this.dataset.value;
        removeSelectedBorderImg();

        // Set Selected Background Value
        selectedBgImgValue = newBgClickerValue;

        // Set Background Image Border Style
        this.children[0].classList.add("selected-bg-img");

        // If Disabled Save Button,
        if (profileBgImgChangeBtn) {
          profileBgImgChangeBtn.classList.remove("disabled");
          profileBgImgChangeBtn.removeAttribute("disabled", false);
        }
      });
    });
  }

  // When User Click Save to Chang Background Image
  if (profileBgImgChangeBtn) {
    profileBgImgChangeBtn.addEventListener("click", function () {
      if (selectedBgImgValue && bgImageModalContainer) {
        profileBgImageContainer.src = selectedBgImgValue;
        profileBgImgInput.value = selectedBgImgValue;
        bgImageModalContainer.hide();
      }
    });
  }

  // When User Click Backgroudn Img
  // we'll show Backgroung Img Changer Modal,
  if (profileBgImageContainer) {
    profileBgImageContainer.addEventListener("click", function () {
      if (bgImageModalContainer) {
        bgImageModalContainer.show();
      }
    });
  }

  // This Function use when other bgImage Click
  // we need to clear first all img border
  function removeSelectedBorderImg() {
    var selectedBgImgContainer = document.querySelector(".selected-bg-img");

    if (selectedBgImgContainer) {
      selectedBgImgContainer.classList.remove("selected-bg-img");
    }
  } // Background Image Changing Process: Finished

  /**
   * Profile Picture Changing Process: Start
   *
   *
   */

  var profilePictureInput = document.getElementById("profile_pic_input");
  var profilePictureImgContainer = document.getElementById("profile_pic");
  var profilePictureLoading = document.getElementById("profile_pic_loading");

  if (profilePictureInput) {
    profilePictureInput.addEventListener("change", function (e) {
      var file = e.target.files[0];

      if (!file) {
        e.target.value = null;
        return;
      }

      var extension = file.name.split(".").pop().toLowerCase();
      var fileExtension = ["jpeg", "jpg", "png"];
      var isValidExtension = fileExtension.some(function (ext) {
        return ext === extension;
      });

      if (isValidExtension) {
        // Show Loading
        if (profilePictureLoading) {
          profilePictureLoading.classList.remove("d-none");
        }

        var formData = new FormData();
        formData.append("file", file);
        // File Uploading
        axios
          .post("/user/profile/image", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then(function () {
            // After Loading We Preshow Image
            if (profilePictureLoading) {
              profilePictureLoading.classList.add("d-none");
            }
            if (profilePictureImgContainer) {
              profilePictureImgContainer.src = URL.createObjectURL(file);
            }
          });
      } else {
        e.target.value = null;
        alert("Not Valid Image File");
        if (profilePictureLoading) {
          profilePictureLoading.classList.remove("d-none");
        }
      }
    });
  } // Profile Picture Changing Process: Finished

  /**
   * Recipes Steps Added Proecess: Start
   *
   *
   */

  var stepsInput = document.getElementById("steps_input");
  var stepsAddButton = document.getElementById("steps_add_button");
  var stepsListContainer = document.getElementById("steps_list_container");
  var stepsList = [];
  var stepsOldRequests = document.getElementById("old_request_steps");

  if (stepsOldRequests) {
    try {
      var oldRequestSteps = stepsOldRequests.innerHTML;
      stepsList = JSON.parse(oldRequestSteps);
      stepsList.forEach(function (data) {
        addMakeStepList(data.value, data.id);
      });
    } catch (e) {
      console.log(e);
    }
  }

  // If Steps Input on click enter
  if (stepsInput) {
    stepsInput.addEventListener("keypress", function (e) {
      // If type Enter, We'll Add New Steps
      if (e.key === "Enter") {
        e.preventDefault();

        // If value is not valid
        if (!e.target.value.trim()) {
          return;
        }
        addMakeStepList(e.target.value.trim());

        // Clean Up Value
        e.target.value = "";
      }
      // var stepsValue = e.target.value;
    });
  }

  if (stepsAddButton && stepsInput) {
    stepsAddButton.addEventListener("click", function () {
      if (!stepsInput.value.trim()) {
        return;
      }

      addMakeStepList(stepsInput.value.trim());

      // Clean Up Value
      stepsInput.value = "";
    });
  }

  function addMakeStepList(value, oldId) {
    var id = oldId ? oldId : makeUiD();
    if (!oldId) {
      stepsList.push({ id: id, value: value });
    }

    var stepChidClassList =
      "list-group-item d-flex justify-content-between align-items-center";
    var setpChildSpanClass = "badge bg-danger rounded-pill close-btn-steps-btn";

    var li = document.createElement("li", {});
    stepChidClassList.split(" ").forEach(function (cls) {
      li.classList.add(cls);
    });

    var span = document.createElement("span", {});
    setpChildSpanClass.split(" ").forEach(function (cls) {
      span.classList.add(cls);
    });

    span.innerHTML = "X";
    span.addEventListener("click", function () {
      stepsList = stepsList.filter(function (ingredient) {
        return ingredient.id !== id;
      });
      li.remove();
    });

    li.append(value);
    li.append(span);
    stepsListContainer.append(li);
  } // Steps Added Process: Finished

  /**
   * Ingredients Added Process: Start
   *
   *
   */
  var ingredientInput = document.getElementById("ingredients_input");
  var ingredientAddedBtn = document.getElementById("ingredients_add_button");
  var ingredientsListContainer = document.getElementById(
    "ingredients_list_container"
  );
  var ingredientList = [];
  var ingredientOldRequest = document.getElementById("old_request_ingredients");

  if (ingredientOldRequest) {
    try {
      var oldRequestSteps = ingredientOldRequest.innerHTML;
      ingredientList = JSON.parse(oldRequestSteps);
      ingredientList.forEach(function (data) {
        addMakeIngredientList(data.value, data.id);
      });
    } catch (e) {
      console.log(e);
    }
  }

  // If Ingredients Input on click enter
  if (ingredientInput) {
    ingredientInput.addEventListener("keypress", function (e) {
      // If type Enter, We'll Add New Ingredients
      if (e.key === "Enter") {
        e.preventDefault();

        // If value is not valid
        if (!e.target.value.trim()) {
          return;
        }
        addMakeIngredientList(e.target.value.trim());

        // Clean Up Value
        e.target.value = "";
      }
      // var IngredientsValue = e.target.value;
    });
  }

  if (ingredientAddedBtn && ingredientInput) {
    ingredientAddedBtn.addEventListener("click", function () {
      if (!ingredientInput.value.trim()) {
        return;
      }

      addMakeIngredientList(ingredientInput.value.trim());

      // Clean Up Value
      ingredientInput.value = "";
    });
  }

  function addMakeIngredientList(value, oldId) {
    var id = oldId ? oldId : makeUiD();
    if (!oldId) {
      ingredientList.push({ id: id, value: value });
    }

    var stepChidClassList =
      "list-group-item d-flex justify-content-between align-items-center";
    var setpChildSpanClass = "badge bg-danger rounded-pill close-btn-steps-btn";

    var li = document.createElement("li", {});
    stepChidClassList.split(" ").forEach(function (cls) {
      li.classList.add(cls);
    });

    var span = document.createElement("span", {});
    setpChildSpanClass.split(" ").forEach(function (cls) {
      span.classList.add(cls);
    });

    span.innerHTML = "X";
    span.addEventListener("click", function () {
      ingredientList = ingredientList.filter(function (ingredient) {
        return ingredient.id !== id;
      });
      li.remove();
    });

    li.append(value);
    li.append(span);
    ingredientsListContainer.append(li);
  } // Ingredients Added Process: Finished

  /**
   * When Submit : Recipe Form Process
   */
  var recipeForm = document.querySelector(".recipe_form");

  // Checking Recipe Form
  if (recipeForm) {
    recipeForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var stepValues = document.getElementById("steps_value_container");
      var ingValues = document.getElementById("ingredients_value_container");

      stepValues.value = stepsList.length ? JSON.stringify(stepsList) : "";
      ingValues.value = ingredientList.length
        ? JSON.stringify(ingredientList)
        : "";
      console.log(stepsList);
      console.log(ingredientList);

      e.target.submit();
    });
  }

  /**
   * Something: Start
   */
});
