function MyNode() {
    this.addInput("input", "number");
    this.addOutput("output", "number");
    this.properties = {};
}

MyNode.title = "Task B";

MyNode.prototype.onExecute = function() {
    let input = this.getInputData(0);
    this.setOutputData(0, input * 2); // 示例：输出是输入的两倍
}

LiteGraph.registerNodeType("category/Task B", MyNode);
