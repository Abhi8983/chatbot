from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

# Predefined questions and answers
qa_pairs = {
    "Why are sodium (Na) and sulfur (S) considered advantageous for battery technology?": "Sodium and sulfur are advantageous because they are abundant and readily available, reducing the cost and environmental impact associated with battery production.",
    "How do the theoretical and practical energy densities of RT-Na/S batteries compare to other battery technologies?": "RT-Na/S batteries have a theoretical energy density of approximately 170 Wh/kg and a practical energy density of approximately 70 Wh/kg, making them competitive with Lithium-Ion and other battery technologies in terms of energy storage capacity.",
    "Why is the practical energy density of RT-Na/S batteries lower than the theoretical value?": "The practical energy density is lower than the theoretical value due to real-world inefficiencies such as incomplete utilization of active materials, energy losses during charging and discharging, and other factors that reduce the overall energy storage capacity.",
    "What challenges might need to be addressed to improve the practical energy density of RT-Na/S batteries?": "Challenges include enhancing the electrochemical stability, improving the conductivity of sulfur, preventing polysulfide shuttle effect, and optimizing the electrode architecture to fully utilize the theoretical capacity.",
    "How do the energy densities of RT-Na/S batteries compare to those of Li-ion and Na-ion batteries?": "RT-Na/S batteries have a higher theoretical energy density than Na-ion batteries and are competitive with Li-ion batteries. However, the practical energy density of RT-Na/S batteries is currently lower than that of Li-ion batteries but has the potential for improvement.",
    "What is the primary function of beta-alumina in a Na-S battery?": "Beta-alumina acts as a solid electrolyte that allows sodium ions (Na⁺) to pass through while preventing the electrons from moving directly between the electrodes, thereby forcing them to travel through the external circuit to generate electric current.",
    "How does the Na-S battery achieve energy storage and release during the discharge and charge cycles?": "During discharge, sodium atoms at the negative electrode lose electrons and migrate as ions through the beta-alumina to the positive electrode, where they react with sulfur to form sodium polysulfides. The reverse reactions occur during charging, restoring sodium and sulfur at their respective electrodes.",
    "What are the key chemical reactions involved in the operation of a Na-S battery?": r"The key reactions are: Discharge: \( 2Na \rightarrow 2Na^+ + 2e^- \) (oxidation at the anode) and \( xS + 2Na^+ + 2e^- \rightarrow Na_2S_x \) (reduction at the cathode). Charge: The reverse of the discharge reactions.",
    "Why are electrons forced to flow through the external circuit in a Na-S battery?": "Electrons are forced to flow through the external circuit because the beta-alumina solid electrolyte only allows the passage of sodium ions, not electrons. This separation of ion and electron pathways ensures that the electrons travel through the external load, generating electrical power.",
    "What is the role of sulfur in the positive electrode during the discharge cycle?": "Sulfur acts as the cathode material that undergoes reduction by gaining electrons and reacting with sodium ions to form sodium polysulfides, thus facilitating the storage of electrical energy.",
    "How does the energy density of Na-S batteries compare to other battery technologies?": "Na-S batteries typically have higher theoretical energy densities compared to many other battery technologies, making them suitable for applications requiring high energy storage. However, practical energy densities are lower due to real-world inefficiencies and material limitations.",
    "What are the advantages of using sodium as an anode material in batteries?": "Sodium is abundant, low-cost, and has favorable electrochemical properties that make it a promising alternative to lithium in battery applications. It also allows for the development of batteries with potentially higher energy densities.",
    "Can you describe the process that occurs at the positive electrode during charging?": "During charging, sodium polysulfides at the positive electrode decompose, releasing sodium ions and electrons. Sulfur is deposited back at the positive electrode, and the released sodium ions migrate through the electrolyte to the negative electrode, where they are reduced to metallic sodium.",
    "Why do HT-Na-S batteries require external heating systems?": "HT-Na-S batteries require external heating systems to maintain an operational temperature range of 300-350°C, which is necessary for the proper functioning of the battery’s chemical reactions.",
    "What impact does the need for high operating temperatures have on the system design and operational costs?": "The need for high operating temperatures adds complexity to the system design, necessitating robust thermal insulation and external heating systems. This increases the operational costs due to constant energy consumption for heating.",
    "How does the requirement for thermal insulation affect HT-Na-S batteries?": "The requirement for thermal insulation to maintain high temperatures adds bulk and weight to the battery system, making it less efficient and more cumbersome.",
    "What are the safety risks associated with HT-Na-S batteries?": "Operating at high temperatures poses safety risks such as potential malfunctions or leaks. Molten sodium can react violently with water, creating a significant fire hazard.",
    "How do startup and shutdown times compare between HT-Na-S batteries and room-temperature batteries?": "HT-Na-S batteries have slower startup and shutdown times because they need to reach and maintain high operating temperatures, unlike room-temperature batteries, which do not have this requirement.",
    "Why do HT-Na-S batteries have a higher overall energy footprint?": "HT-Na-S batteries have a higher overall energy footprint due to the constant energy required for heating to maintain the high operating temperatures, making them less energy-efficient compared to room-temperature batteries.",
    "What are the main challenges in maintaining the high operating temperatures of HT-Na-S batteries?": "The main challenges include ensuring robust thermal insulation, managing the added bulk and weight, mitigating safety risks from potential malfunctions or leaks, and managing the increased energy consumption for heating.",
    "In what scenarios might HT-Na-S batteries still be considered despite these drawbacks?": "HT-Na-S batteries might still be considered in scenarios where high energy density and specific operational requirements justify the complexity, cost, and safety measures, such as in large-scale energy storage or industrial applications.",
    "What are the main components of an RT-Na-S battery as shown in the schematic?": "The main components are the negative electrode (sodium Na), solid electrolyte (beta-alumina), and the positive electrode (sulfur S).",
    "Describe the chemical reaction occurring at the negative electrode during the discharge process.": r"At the negative electrode, sodium atoms lose electrons to form sodium ions (Na^+). The reaction is \( 2Na \rightarrow 2Na^+ + 2e^- \).",
    "How do sodium ions (Na⁺) move within the RT-Na-S battery during discharge?": "Sodium ions migrate from the negative electrode through the solid electrolyte (beta-alumina) to the positive electrode.",
    "What happens at the positive electrode during the discharge process of an RT-Na-S battery?": "At the positive electrode, sodium ions (Na⁺) react with sulfur (S) to form sodium polysulfides (Na₂Sₓ) while electrons flow through the external circuit to complete the reaction.",
    "Explain the significance of the voltage profile shown in Figure 3b during the discharge process.": "The voltage profile illustrates the cell voltage at different states of discharge. It shows how the voltage changes as various sodium polysulfides (Na₂Sₓ) are formed during discharge, indicating the electrochemical reactions occurring within the cell.",
    "What is the initial voltage of the Na/S cell at the beginning of the discharge process?": "The initial voltage of the Na/S cell is approximately 2.075 V when Na₂S₅ is present.",
    "How does the voltage change as the discharge progresses in the Na/S cell?": "As discharge progresses, the voltage decreases from around 2.075 V to 1.74 V, corresponding to the formation of different phases such as Na₂S₄ and Na₂S₃.",
    "What phases are present at different stages of discharge in the Na/S cell?": "During discharge, phases like Na₂S₅, Na₂S₄, and Na₂S₃ are formed sequentially as indicated by the voltage profile.",
    "Why is it important to understand the voltage profile of a Na/S cell?": "Understanding the voltage profile is crucial for optimizing battery performance, predicting remaining capacity, and ensuring safe operation by monitoring the electrochemical reactions within the cell.",
    "How does the electron flow in the external circuit contribute to the battery's functionality during discharge?": "The flow of electrons through the external circuit provides electrical power to an external load, which is the primary function of the battery during discharge.",
    "What is the primary difference in the operating temperature ranges of HT-Na-S and RT-Na-S batteries?": "HT-Na-S batteries operate at high temperatures ranging from 300°C to 350°C, whereas RT-Na-S batteries operate at much lower temperatures from 20°C to 60°C.",
    "Why do HT-Na-S batteries require a beta-alumina solid electrolyte?": "Beta-alumina solid electrolyte is stable and effective at high temperatures, facilitating the movement of sodium ions between the electrodes in HT-Na-S batteries.",
    "What type of electrolyte is used in RT-Na-S batteries and why?": "RT-Na-S batteries use a solid electrolyte that functions efficiently at room temperatures (20°C to 60°C), ensuring ionic conductivity without the need for high temperatures.",
    "How does the state of the sodium anode differ between HT-Na-S and RT-Na-S batteries?": "In HT-Na-S batteries, the sodium anode is in a molten state due to high operating temperatures. In RT-Na-S batteries, the sodium anode is in a solid state suitable for room temperature operations.",
    "What materials are used for the sulfur cathode in both HT-Na-S and RT-Na-S batteries?": "HT-Na-S batteries use porous carbon with sulfur or sulfur-based compounds, while RT-Na-S batteries use sulfur or sulfur-based compounds likely optimized for lower temperature functionality.",
    "What are the advantages of using RT-Na-S batteries over HT-Na-S batteries?": "RT-Na-S batteries operate at lower temperatures, reducing the need for external heating systems, complex thermal insulation, and associated safety risks. This can lead to simpler designs, lower costs, and improved safety.",
    "Why is it important to maintain high temperatures in HT-Na-S batteries?": "High temperatures in HT-Na-S batteries are necessary to keep the sodium anode in a molten state and to ensure efficient ionic conductivity through the beta-alumina solid electrolyte.",
    "What are the challenges associated with the high operating temperatures of HT-Na-S batteries?": "Challenges include the need for robust thermal insulation, constant energy consumption for heating, safety risks from high-temperature operations, and slower startup and shutdown times due to the time required to reach operating temperatures.",
    "How do the materials used in the sulfur cathode of HT-Na-S and RT-Na-S batteries contribute to their respective performance?": "In HT-Na-S batteries, porous carbon with sulfur compounds allows efficient electron and ion transport at high temperatures. In RT-Na-S batteries, sulfur or sulfur-based compounds are used in a manner that optimizes their performance at lower temperatures, potentially with different structural characteristics.",
    "In what applications might HT-Na-S batteries be preferred over RT-Na-S batteries despite their higher operational challenges?": "HT-Na-S batteries might be preferred in applications requiring high energy densities and where the operational environment can accommodate high temperatures, such as in certain industrial energy storage systems.",
    "What is the starting material used to produce microporous carbon for RT-Na-S batteries?": "The starting material is sucrose (C12H22O11).",
    "What is the role of sulfuric acid in the process?": "Sulfuric acid is used to dehydrate sucrose, which results in the formation of amorphous carbon.",
    "At what temperature and duration is the dehydration process carried out?": "The dehydration process is carried out at 120°C for 10 hours.",
    "What is the next step after dehydration and what conditions are used?": "The next step is pyrolysis, which is conducted under low-pressure argon flow at 850°C for 2 hours.",
    "What is the purpose of the pyrolysis step?": "Pyrolysis converts the amorphous carbon into ordered microporous carbon spheres.",
    "What are the characteristics of the carbon spheres formed after pyrolysis?": "The carbon spheres have uniform micropores with a size of approximately 0.5 nm.",
    "How is sulfur integrated into the microporous carbon spheres?": "Sulfur is infiltrated into the microporous carbon spheres to form sulfur-infiltrated spheres (S@C).",
    "Why are microporous carbon spheres important for RT-Na-S batteries?": "Microporous carbon spheres provide a high surface area and uniform pore structure, which enhance the performance and capacity of RT-Na-S batteries by facilitating better sulfur utilization and improving the conductivity.",
    "Can you explain the significance of using low-pressure argon flow during pyrolysis?": "Using low-pressure argon flow helps to prevent oxidation and ensures the formation of high-quality carbon structures.",
    "What is the expected outcome of using sucrose-derived microporous carbon in RT-Na-S batteries?": "The expected outcome is improved battery performance, including higher capacity, better cycling stability, and enhanced sulfur utilization.",
    "What is the method used to infiltrate sulfur into the microporous carbon?": "Sulfur is infiltrated using an isothermal vapor phase process.",
    "What temperature and duration are used for the sulfur infiltration process?": "The sulfur infiltration process is carried out at 175°C for 1 hour.",
    "What is the weight percentage of sulfur confined within the micropores after infiltration?": "The process results in 35 wt% sulfur confined within the micropores.",
    "Why is uniform sulfur distribution important in sodium-sulfur batteries?": "Uniform sulfur distribution is crucial for high performance and cycling stability as it ensures consistent electrochemical reactions and prevents issues such as sulfur agglomeration and capacity fading.",
    "What does Figure E show in the context of sulfur infiltration?": "Figure E is a composite image that shows the distribution of carbon and sulfur within the microporous carbon spheres.",
    "What is the significance of Figures F and G in the image?": "Figure F highlights the carbon structure, while Figure G highlights the sulfur distribution within the carbon structure, illustrating how sulfur is uniformly dispersed in the micropores.",
    "Describe what the graph in Figure H indicates.": "The graph in Figure H shows the normalized counts of carbon and sulfur across a distance of 500 nm. It indicates the uniform distribution of sulfur within the carbon micropores, which is essential for the battery's performance.",
    "How does the sulfur infiltration process enhance the performance of sodium-sulfur batteries?": "The process ensures that sulfur is uniformly distributed within the carbon micropores, enhancing the electrochemical performance, increasing capacity, and improving cycling stability of the batteries.",
    "What challenges might arise if sulfur is not uniformly distributed in the carbon micropores?": "If sulfur is not uniformly distributed, it can lead to uneven electrochemical reactions, sulfur agglomeration, reduced battery capacity, and poor cycling stability.",
    "How does the isothermal vapor phase process contribute to the uniform distribution of sulfur?": "The isothermal vapor phase process allows sulfur to infiltrate the micropores evenly by maintaining a consistent temperature and vapor environment, facilitating uniform sulfur deposition within the carbon structure.",
    "What does Figure A represent in the context of the Na-S battery?": "Figure A represents the cyclic voltammetry (CV) curves showing the current density vs. potential for the first two cycles of the Na-S battery. The peaks correspond to the formation and reduction of different sodium polysulfides.",
    "What are the main observations from the cyclic voltammetry (CV) curves in Figure A?": "The CV curves show distinct peaks corresponding to different sodium polysulfides, indicating the electrochemical reactions taking place during the charge and discharge cycles. The consistent peaks in the second cycle suggest good reversibility.",
    "What information does Figure B provide about the Na-S battery?": "Figure B shows the charge-discharge profiles at different C-rates (0.1C, 0.25C, 0.5C, 1C), demonstrating the battery's potential vs. capacity. It highlights how the capacity changes with different rates of charge and discharge.",
    "How does the capacity of the Na-S battery vary with different C-rates according to Figure B?": "The capacity decreases with increasing C-rates, indicating that the battery can deliver higher capacity at lower C-rates, but the capacity drops as the charge-discharge rate increases.",
    "What is shown in Figure C regarding the cycling performance of the Na-S battery?": "Figure C shows the capacity and Coulombic efficiency vs. cycle number for various C-rates (0.1C, 0.25C, 0.5C, 1C). It demonstrates the battery's stability and efficiency over multiple cycles.",
    "What does the Coulombic efficiency indicate in Figure C?": "The Coulombic efficiency, shown as a percentage, indicates the efficiency of charge transfer in the battery. A high Coulombic efficiency close to 100% suggests minimal loss of active material and high reversibility.",
    "Describe the long-term cycling performance as shown in Figure D.": "Figure D presents the long-term cycling performance at 0.1C, showing the capacity vs. cycle number for both charge and discharge cycles. It highlights the battery's ability to maintain capacity over an extended number of cycles with high Coulombic efficiency.",
    "How does the Na-S battery perform in terms of capacity retention over extended cycles as shown in Figure D?": "The Na-S battery shows good capacity retention over extended cycles, indicating its long-term cycling stability. The charge and discharge capacities remain relatively stable, and the Coulombic efficiency remains high.",
    "What can be inferred about the effectiveness of sucrose-derived microporous carbon in Na-S batteries from these figures?": "The figures demonstrate that sucrose-derived microporous carbon effectively enhances the Na-S battery's performance, providing high capacity, good cycling stability, and high Coulombic efficiency. This indicates the material's suitability for improving Na-S battery performance."
}


def find_answer(question):
    # Simple keyword matching
    for q, a in qa_pairs.items():
        if all(word.lower() in q.lower() for word in question.split()):
            return a
    return "Sorry, I don't have an answer for that question."


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "Please provide a question"}), 400

    answer = find_answer(question)
    return jsonify({"question": question, "answer": answer})


if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
