const BASE_URL = "http://127.0.0.1:5000";
        let ruleCount = 0;  // Track the number of rules created

        function createRule() {
            const ruleString = document.getElementById("ruleString").value;
            fetch(`${BASE_URL}/create_rule`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ rule_string: ruleString })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("output").innerText += `Create Rule Response: ${JSON.stringify(data)}\n`;
                renderAST(data.ast);  // Call to render the AST

                // Update the rules list
                ruleCount++;
                const ruleElement = document.createElement("div");
                ruleElement.textContent = `Rule ${ruleCount}: ${ruleString} (ID: ${data.id})`;
                document.getElementById("rulesList").appendChild(ruleElement);
            })
            .catch(error => {
                document.getElementById("output").innerText += `Error: ${error}\n`;
            });
        }

        function combineRules() {
            const ruleIds = document.getElementById("ruleIds").value.split(',').map(id => parseInt(id.trim()));
            fetch(`${BASE_URL}/combine_rules`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ rule_ids: ruleIds })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("output").innerText += `Combine Rules Response: ${JSON.stringify(data)}\n`;
            })
            .catch(error => {
                document.getElementById("output").innerText += `Error: ${error}\n`;
            });
        }

        function evaluateRule() {
            const megaRuleId = parseInt(document.getElementById("megaRuleId").value);
            const data = document.getElementById("data").value;
            try {
                const dataJson = JSON.parse(data);
                fetch(`${BASE_URL}/evaluate_rule`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ rule_id: megaRuleId, data: dataJson })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("output").innerText += `Evaluate Rule Response: ${JSON.stringify(data)}\n`;
                })
                .catch(error => {
                    document.getElementById("output").innerText += `Error: ${error}\n`;
                });
            } catch (error) {
                document.getElementById("output").innerText += `JSON Decode Error: ${error}\n`;
            }
        }

        function modifyRule() {
            const ruleId = parseInt(document.getElementById("modifyRuleId").value);
            const newRuleString = document.getElementById("newRuleString").value;
            fetch(`${BASE_URL}/modify_rule`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ rule_id: ruleId, new_rule_string: newRuleString })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("output").innerText += `Modify Rule Response: ${JSON.stringify(data)}\n`;
            })
            .catch(error => {
                document.getElementById("output").innerText += `Error: ${error}\n`;
            });
        }

        function renderAST(ast) {
            // Clear previous AST
            d3.select("#astContainer").selectAll("*").remove();

            const parsedAST = JSON.parse(ast);
            const treeData = toTreeStructure(parsedAST);
            const svg = d3.select("#astContainer").append("svg").attr("width", 600).attr("height", 400);
            const g = svg.append("g").attr("transform", "translate(40,0)");

            const tree = d3.tree().size([300, 200]);
            const root = d3.hierarchy(treeData);
            tree(root);

            // Links
            g.selectAll(".link")
                .data(root.links())
                .enter().append("path")
                .attr("class", "link")
                .attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x));

            // Nodes
            const node = g.selectAll(".node")
                .data(root.descendants())
                .enter().append("g")
                .attr("class", d => "node" + (d.children ? " node--internal" : " node--leaf"))
                .attr("transform", d => "translate(" + d.y + "," + d.x + ")");

            node.append("circle")
                .attr("r", 5);

            // Change text color to white
            node.append("text")
                .attr("dy", 3)
                .attr("x", d => d.children ? -8 : 8)
                .style("text-anchor", d => d.children ? "end" : "start")
                .style("fill", "#ffffff")  // Change text color to white
                .text(d => d.data.name);
        }

        function toTreeStructure(node) {
            // Helper function to convert AST to tree structure for D3
            if (node.type === 'operand') {
                return { name: node.value };
            }
            const children = [node.left, node.right].filter(Boolean).map(toTreeStructure);
            return { name: node.value, children: children };
        }