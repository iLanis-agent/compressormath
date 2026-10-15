var CompressorMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  var DERATE = 0.8;
  function cfmPlan(sticker) {
    if (!pos(sticker)) return { error: "the sticker CFM must be above zero" };
    return { cfm90: r1(sticker * DERATE) };
  }
  function renderCfm(r, sticker) {
    return "The " + jsnum(sticker) + " CFM on the box was measured at 40 PSI; your tools breathe at 90, where the pump honestly gives about "
      + jsnum(r.cfm90) + " CFM.";
  }
  function recoveryPlan(tankGal, cutIn, cutOut, cfm) {
    if (!pos(tankGal)) return { error: "the tank size must be above zero" };
    if (!num(cutIn)) return { error: "the cut-in pressure must be a number" };
    if (!num(cutOut)) return { error: "the cut-out pressure must be a number" };
    if (cutOut <= cutIn) return { error: "the cut-out must beat the cut-in" };
    if (!pos(cfm)) return { error: "the pump CFM must be above zero" };
    var freeAirCuFt = tankGal * (cutOut - cutIn) / 14.7 / 7.48;
    return { freeAir: r1(freeAirCuFt), seconds: r1(freeAirCuFt / cfm * 60) };
  }
  function renderRecovery(r, tankGal, cutIn, cutOut, cfm) {
    return "The " + jsnum(tankGal) + "-gallon tank climbing from " + jsnum(cutIn) + " to " + jsnum(cutOut) + " PSI holds about "
      + jsnum(r.freeAir) + " cubic feet of free air - at " + jsnum(cfm) + " honest CFM that is about " + jsnum(r.seconds)
      + " seconds of recovery the tool feels every cycle.";
  }
  function dutyPlan(toolCfm, pumpCfm) {
    if (!pos(toolCfm)) return { error: "the tool demand must be above zero" };
    if (!pos(pumpCfm)) return { error: "the pump CFM must be above zero" };
    var pct = toolCfm / pumpCfm * 100;
    var verdict = pct <= 50 ? "the tool runs all day and the pump barely works"
      : pct <= 80 ? "the pump keeps up, with pauses for the tank to catch its breath"
      : pct <= 100 ? "the pump barely keeps up - long runs empty the tank"
      : "the pump cannot feed it - the tool starves mid-pass";
    return { pct: r1(pct), verdict: verdict };
  }
  function renderDuty(r, toolCfm, pumpCfm) {
    return "The tool asks " + jsnum(toolCfm) + " CFM against the pump's honest " + jsnum(pumpCfm) + " - a duty of " + jsnum(r.pct)
      + "% means " + r.verdict + ".";
  }
  return { cfmPlan: cfmPlan, renderCfm: renderCfm, recoveryPlan: recoveryPlan, renderRecovery: renderRecovery, dutyPlan: dutyPlan, renderDuty: renderDuty };
})();
if (typeof module !== "undefined" && module.exports) module.exports = CompressorMath;
