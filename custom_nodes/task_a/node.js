function MyNode() {
    this.addInput("input", "number");
    this.addOutput("output", "number");
    this.addWidget("progress", "progress", 0, function (v) { }, { min: 0, max: 100 });
    this.properties = {};
}

MyNode.title = "Task A";

MyNode.prototype.onExecute = function () {
    let input = this.getInputData(0);
    this.setOutputData(0, input * 2); // 示例：输出是输入的两倍
}

LiteGraph.registerNodeType("category/Task A", MyNode);
