const allURL = [
  "https://writing9.com/text/64a8188465a98e0018b125eb-some-people-think-the-government-should-pay-for-healthcare-and",
  "https://writing9.com/text/64a816d165a98e0018b125e5-topic-some-people-believe-that-visitors-to-other-countries-should",
  "https://writing9.com/text/64a8155c65a98e0018b125db-some-people-say-that-in-our-modern-age-it-is",
  "https://writing9.com/text/64a80fad65a98e0018b125d0-social-media-addiction-many-people-believe-that-social-networking-sites",
  "https://writing9.com/text/64a808a165a98e0018b125bf-allowing-young-children-to-do-an-enjoyable-activity-can-develop",
  "https://writing9.com/text/64a7e2ca65a98e0018b12565-some-people-say-that-parents-have-the-most-important-role",
  "https://writing9.com/text/64a7106ebeee5d0018e1a66f-in-the-future-books-will-exist-only-on-computers-do-you",
  "https://writing9.com/text/64a7b75bbeee5d0018e1a763-money-spent-on-space-exploration-is-a-complete-waste-governments",
  "https://writing9.com/text/64a77c72beee5d0018e1a6da-prison-is-the-best-punishment-for-criminals-to-what-extent-you",
  "https://writing9.com/text/64a818e865a98e0018b125ef-information-technology-enables-many-people-to-do-their-work-outside",
  "https://writing9.com/text/64a8129b65a98e0018b125d4-large-companies-should-pay-higher-salaries-to-ceos-and-executives",
  "https://writing9.com/text/64a8081a65a98e0018b125bb-children-who-grow-up-in-families-which-are-short-of",
  "https://writing9.com/text/64a8035c65a98e0018b125b1-some-people-believe-that-everyone-has-a-right-to-have",
  "https://writing9.com/text/64a802eb65a98e0018b125af-nowadays-older-people-who-need-employment-have-to-compete-with",
  "https://writing9.com/text/64a7e37c65a98e0018b1256b-some-people-think-that-wild-animals-should-not-be-keptin",
  "https://writing9.com/text/64a7d873beee5d0018e1a7c7-machine-translation-mt-is-slower-and-less-accurate-than-human",
  "https://writing9.com/text/64a7cfd1beee5d0018e1a7a6-some-people-think-computer-games-have-negative-impacts-on-children",
  "https://writing9.com/text/64a7c191beee5d0018e1a776-some-people-believe-that-school-children-should-not-be-given",
  "https://writing9.com/text/64a7aa2bbeee5d0018e1a746-in-some-countries-an-increasing-number-of-people-are-suffering",
  "https://writing9.com/text/64a8108565a98e0018b125d2-these-days-people-work-in-more-than-one-job-and",
  "https://writing9.com/text/64a7fe1f65a98e0018b125a8-human-activities-have-a-negative-effect-on-plant-and-animal",
  "https://writing9.com/text/64a7f38565a98e0018b1258e-in-number-of-countries-some-people-think-it-is-necessary",
  "https://writing9.com/text/64a7e54c65a98e0018b12571-some-people-say-that-parents-have-the-most-important-role",
  "https://writing9.com/text/64a7d413beee5d0018e1a7b8-some-people-say-that-music-is-a-good-way-of",
  "https://writing9.com/text/64a7c75abeee5d0018e1a781-in-the-modern-world-it-is-possible-to-shop-work",
  "https://writing9.com/text/64a7b327beee5d0018e1a75d-in-contemporary-society-everyone-should-have-equal-opportunities-in-education",
  "https://writing9.com/text/64a7acf7beee5d0018e1a74f-in-many-countries-formal-exams-are-used-to-access-students",
  "https://writing9.com/text/64a7a3c4beee5d0018e1a734-some-ex-prisoners-commit-crimes-after-being-released-from-the-prison",
  "https://writing9.com/text/64a7a0b2beee5d0018e1a72b-nowadaya-both-men-and-women-spend-a-lot-of-money",
  "https://writing9.com/text/64a749dcbeee5d0018e1a6a0-school-children-are-becoming-far-too-dependent-on-computers",
];

const axios = require("axios");
const cheerio = require("cheerio");
const fs = require("fs");
const allArr = [];

function convertObjectToCSV(objArray) {
  let csvContent = "";

  // Extract headers from the first object
  const headers = Object.keys(objArray[0]);
  csvContent += headers.join(",") + "\n";

  // Extract values from each object and format as CSV rows
  objArray.forEach((obj) => {
    const row = headers.map((header) => {
      const value = obj[header];
      return value ? `"${value}"` : "";
    });
    csvContent += row.join(",") + "\n";
  });

  return csvContent;
}

allURL.forEach((url) => {
  async function getHTML() {
    const { data: html } = await axios.get(url);
    return html;
  }

  getHTML()
    .then((res) => {
      const $ = cheerio.load(res);
      const data0 = $(".page-text__question").text();
      const data1 = $(".page-text__text").text();
      const data2 = $(".page-draft-text-analyzer__band").text();
      // const data3 = $(
      //   ".page-draft-text-analyzer__section-container:eq(0)"
      // ).text();
      const data4 = $(
        ".page-draft-text-analyzer__section-container:eq(2)"
      ).text();
      const data5 = $(
        ".page-draft-text-analyzer__section-container:eq(3)"
      ).text();
      // const data6 = $(
      //   ".page-draft-text-analyzer__section-container:eq(4)"
      // ).text();
      // const data7 = $(
      //   ".page-draft-text-analyzer__section-container:eq(5)"
      // ).text();

      const obj = {};
      obj.question = data0.replace(/\n/g, "");
      obj.main = data1.replace(/\n/g, "");
      obj.band = data2.substring(0, 3);
      // obj.structure = data3;
      obj.coherence = data4;
      obj.lexical = data5;
      // obj.grammatical = data6;
      // obj.task = data7;

      allArr.push(obj);
    })
    .then(() => {
      // console.log(allArr);
      // const csv = convertObjectToCSV(allArr);
      // fs.writeFileSync("data.csv", csv);
      fs.writeFile("data.json", JSON.stringify(allArr), (err) => {
        if (err) {
          console.error("Error writing JSON file:", err);
          return;
        }
        console.log("JSON file has been saved successfully.");
      });
    });
});
