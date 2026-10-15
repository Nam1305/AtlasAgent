# Checklist kiểm tra tiến độ học AI Agent

Checklist này bám theo `Plan2.md`. Đánh dấu `[x]` chỉ khi tự giải thích hoặc tự chạy được, không đánh dấu chỉ vì đã đọc qua.

## Cách sử dụng

Sau mỗi tuần:

1. Tự trả lời phần **Hiểu** mà không nhìn tài liệu.
2. Chạy lại phần **Làm được** từ một terminal mới.
3. Chạy toàn bộ phần **Kiểm chứng** và lưu kết quả.
4. Chỉ chuyển tuần khi hoàn thành tất cả mục **Bắt buộc để qua tuần**.

---

## Tuần 0 — Nền tảng và dựng project

### Hiểu

- [x] Giải thích được sự khác nhau giữa chatbot gọi LLM một lần và AI agent.
- [x] Giải thích được `system`, `user`, `assistant` message.
- [x] Giải thích được token và context window ảnh hưởng thế nào đến chi phí và câu trả lời.
- [x] Giải thích được structured output và lý do phải validate output.
- [x] Phân biệt được workflow định trước và agent tự chọn hành động.
- [x] Giải thích được skeleton project và model gateway.

### Làm được

- [x] Viết 10 user stories, chọn 1 use case chính và 3 use case phụ.
- [ ] Cấu hình Gemini API free tier, một agent framework và một vector store cho MVP.
- [x] Chọn một OCR engine cho PDF scan và ghi lại lý do chọn.
- [x] Tạo skeleton project, môi trường Python và `.env.example`.
- [x] API key được đọc từ biến môi trường, không hard-code trong code.
- [x] Model gateway nhận messages và trả response đã chuẩn hóa.
- [x] Chatbot một lượt chạy được từ UI.
- [x] Có FastAPI `/health` và `/chat` phiên bản đơn giản.
- [x] Lỗi từ model được trả về dưới dạng lỗi có cấu trúc, không làm sập ứng dụng.
- [x] Đã gom tài liệu mẫu và tạo bộ câu hỏi–đáp án–nguồn cho RAG.

### Kiểm chứng

- [x] Chạy được Web UI và API theo hướng dẫn trong README.
- [x] `/health` trả trạng thái thành công.
- [x] `/chat` trả output đúng Pydantic schema.
- [x] Có log `request_id`, model, token và latency cơ bản.
- [x] Có ít nhất 5 smoke tests và tất cả đều pass.
- [x] Tìm toàn repo không thấy API key thật trong các file được Git theo dõi.

### Bắt buộc để qua tuần

- [x] Chatbot một lượt chạy được end-to-end bằng Web UI và API.
- [x] Có ít nhất 5 smoke tests và tất cả đều pass.
- [x] Output được validate; lỗi model không làm sập server.


---

## Tuần 1 — Agent loop và tool calling

### Hiểu

- [ ] Giải thích được agent loop: chọn action → gọi tool → nhận observation → tiếp tục hoặc dừng.
- [ ] Giải thích được tool/function calling và tool schema.
- [ ] Biết vì sao không nên yêu cầu hoặc lưu chain-of-thought thô.
- [ ] Giải thích được vai trò của allowlist, timeout, `max_steps` và retry budget.
- [ ] Phân biệt được lỗi model, lỗi validate và lỗi khi chạy tool.

### Làm được

- [ ] Tạo `Tool` interface có name, description, input schema và output schema.
- [ ] Tạo `calculator(expression)`.
- [ ] Tạo `search_documents(query, filters)` bản đơn giản hoặc giả lập.
- [ ] Tạo `get_source(source_id)` bản đơn giản hoặc giả lập.
- [ ] Tạo tool registry và chỉ cho phép chạy tool trong allowlist.
- [ ] Viết ReAct loop thủ công, chưa phụ thuộc LangGraph.
- [ ] Validate tool arguments trước khi thực thi.
- [ ] Tool error được chuẩn hóa để agent có thể thử lại hoặc dừng.
- [ ] Loop luôn có điều kiện dừng và giới hạn số bước.
- [ ] Chuyển loop đã hiểu thành các node graph cơ bản.

### Kiểm chứng

- [ ] Calculator xử lý đúng input hợp lệ.
- [ ] Input sai schema bị từ chối an toàn.
- [ ] Tool không có trong registry không thể được gọi.
- [ ] Tool bị treo sẽ timeout.
- [ ] Agent dừng khi chạm `max_steps`.
- [ ] Log có action, observation, duration và status nhưng không có chain-of-thought thô.
- [ ] Bộ 20 câu test nhỏ đạt ít nhất 90% tool selection đúng.

### Bắt buộc để qua tuần

- [ ] Agent tự chọn đúng tool cho câu hỏi tính toán và tìm tài liệu.
- [ ] Không có đường chạy nào tạo loop vô hạn.
- [ ] Unit test tool và integration test agent loop đều pass.

---

## Tuần 2 — RAG, retrieval và memory

### Hiểu

- [ ] Giải thích được embedding, vector store và semantic search.
- [ ] Giải thích được pipeline retrieve → augment → generate.
- [ ] So sánh được fixed-size, recursive và semantic chunking.
- [ ] Giải thích được top-k, metadata filter, reranking và context budget.
- [ ] Phân biệt short-term memory với long-term memory.
- [ ] Hiểu vì sao câu trả lời phải gắn citation với claim.

### Làm được

- [ ] Nạp được PDF, Markdown và TXT.
- [ ] Phát hiện được trang PDF có text layer và trang cần OCR.
- [ ] Trang có text layer được trích trực tiếp; trang scan tự động dùng OCR fallback.
- [ ] PDF trộn trang text và trang scan được xử lý đúng trong cùng một file.
- [ ] Chunk vẫn giữ file, heading, trang, chunk ID và `extraction_method` (`native` hoặc `ocr`).
- [ ] Lưu OCR confidence khi engine cung cấp và xử lý được trang có confidence thấp.
- [ ] So sánh ít nhất hai chiến lược chunking trên cùng tài liệu.
- [ ] Ingest có tính idempotent, không nhân bản cùng một tài liệu.
- [ ] Lưu version tài liệu, OCR engine/config, embedding model và chunking config.
- [ ] Semantic search trả về các chunk liên quan.
- [ ] Có metadata filter và context budget.
- [ ] Có reranking hoặc ít nhất benchmark trước khi quyết định chưa dùng.
- [ ] Câu trả lời chứa source ID/file/trang hoặc chunk phù hợp.
- [ ] Khi thiếu bằng chứng, hệ thống trả “chưa đủ dữ liệu” thay vì đoán.
- [ ] Short-term memory giữ được hội thoại nhiều lượt.
- [ ] Memory được tách namespace theo user/session.

### Kiểm chứng

- [ ] Có ít nhất 20 câu hỏi với đáp án và nguồn chuẩn; mục tiêu tiếp theo là 30 câu.
- [ ] Bộ test có ít nhất một PDF text, một PDF scan và một PDF trộn hai loại trang.
- [ ] Kết quả extraction/OCR giữ đúng page mapping để citation không lệch trang.
- [ ] Đo được chất lượng OCR trên một tập trang scan mẫu và lưu lỗi điển hình.
- [ ] Đo được Recall@5 trên bộ câu hỏi đã gán nguồn.
- [ ] Recall@5 đạt ít nhất 0,80 trên 30 câu trước khi kết thúc tuần.
- [ ] Citation đúng nguồn đạt ít nhất 90%.
- [ ] Test xác nhận hai session không đọc nhầm memory của nhau.
- [ ] Hội thoại dài được cắt/tóm tắt theo context budget.

### Bắt buộc để qua tuần

- [ ] Research Agent trả lời từ tài liệu và có citation kiểm chứng được.
- [ ] Ingest lại cùng tài liệu không tạo dữ liệu trùng.
- [ ] PDF scan được OCR, truy xuất và trích dẫn đúng trang qua pipeline end-to-end.
- [ ] Đạt ngưỡng retrieval, citation và memory isolation ở trên.

---

## Tuần 3 — Workflow đa bước và multi-agent

### Hiểu

- [ ] Giải thích được Plan-and-Execute, Router và Orchestrator/Worker.
- [ ] Giải thích được node, edge, conditional edge, state và checkpoint.
- [ ] Phân biệt rõ trách nhiệm của Supervisor và từng sub-agent.
- [ ] Giải thích được handoff có schema tốt hơn truyền toàn bộ chat tự do.
- [ ] Hiểu lợi ích và rủi ro của self-critique/Reflexion.

### Làm được

- [ ] Tạo state graph có checkpoint theo `session_id` hoặc `run_id`.
- [ ] Router trả một route hợp lệ bằng structured output.
- [ ] Supervisor tạo task có owner, input, expected output, dependency và status.
- [ ] Có Research, Analyst, Writer và Reviewer với trách nhiệm tách biệt.
- [ ] Handoff giữa agent dùng object có schema và artifact reference.
- [ ] Writer chỉ dùng evidence đã thu thập, không tự bịa nguồn.
- [ ] Reviewer chấm correctness, completeness, citation, clarity và safety.
- [ ] Feedback không đạt được route về đúng agent cần sửa.
- [ ] Giới hạn tối đa hai vòng sửa.
- [ ] Có fallback khi agent hoặc tool thất bại.
- [ ] Worker độc lập có thể chạy song song khi không có dependency.

### Kiểm chứng

- [ ] Một yêu cầu phức tạp được phân rã, giao việc, review và sửa tự động.
- [ ] Có thể xem lại graph path của từng run.
- [ ] 100% task kết thúc ở `completed`, `failed` hoặc `skipped`.
- [ ] Không request nào vượt quá hai vòng review.
- [ ] Integration test xác nhận feedback được chuyển đúng node.
- [ ] Có so sánh chất lượng với baseline single-agent.

### Bắt buộc để qua tuần

- [ ] Workflow multi-agent chạy end-to-end trên ít nhất một use case chính.
- [ ] Không có task treo hoặc trạng thái kết thúc mơ hồ.
- [ ] Reviewer thực sự phát hiện và kích hoạt sửa một lỗi có chủ đích.

---

## Tuần 4 — Safety, guardrails và human-in-the-loop

### Hiểu

- [ ] Phân biệt input, output và tool guardrail.
- [ ] Giải thích được prompt injection trực tiếp và gián tiếp.
- [ ] Phân biệt instruction đáng tin với dữ liệu không đáng tin.
- [ ] Giải thích được least privilege, allowlist và sandboxing.
- [ ] Biết hành động nào cần con người phê duyệt.

### Làm được

- [ ] Viết threat model gồm asset, actor, entry point và impact.
- [ ] Gắn trust level cho system prompt, user input, retrieved content và tool output.
- [ ] Retrieved content luôn được coi là dữ liệu, không phải system instruction.
- [ ] Input guardrail kiểm tra kích thước, định dạng và abuse cơ bản.
- [ ] Output guardrail kiểm tra secret, PII và citation.
- [ ] Mọi tool argument đều được validate bằng schema và policy.
- [ ] Mỗi tool có risk level: read-only, reversible write hoặc destructive.
- [ ] Approval Node hiển thị action, target, payload và hậu quả.
- [ ] Thay đổi payload làm mất approval cũ và yêu cầu duyệt lại.
- [ ] Workflow có thể pause, lưu checkpoint và resume.
- [ ] Có policy sandbox trước khi cho phép code execution.

### Kiểm chứng

- [ ] Có adversarial tests cho injection, exfiltration và tool misuse.
- [ ] Prompt injection nằm trong tài liệu không thể điều khiển supervisor trái policy.
- [ ] 100% tool có schema, timeout và risk level.
- [ ] 100% hành động destructive trong test phải qua approval.
- [ ] Bộ test không làm lộ secret hoặc PII giả lập.

### Bắt buộc để qua tuần

- [ ] Injection từ user và tài liệu đều bị vô hiệu hóa trong bộ test.
- [ ] Approval được gắn đúng payload và workflow resume đúng checkpoint.
- [ ] Không có tool nào chạy ngoài allowlist hoặc vượt quyền đã định.

---

## Tuần 5 — Evaluation và observability

### Hiểu

- [ ] Phân biệt offline eval và online monitoring.
- [ ] Phân biệt deterministic grader, human grader và LLM-as-judge.
- [ ] Giải thích được golden dataset, regression test và failure taxonomy.
- [ ] Phân biệt log, metric, trace và span.
- [ ] Hiểu trade-off giữa quality, latency và cost.

### Làm được

- [ ] Tạo golden dataset tối thiểu 80 case theo phân bố trong `Plan2.md`.
- [ ] Mỗi case có expected route/source, required facts và forbidden behavior khi phù hợp.
- [ ] Có deterministic grader cho schema, route, citation và tool call.
- [ ] LLM-as-judge dùng rubric cố định cho relevance và clarity.
- [ ] LLM judge được đối chiếu với một tập nhỏ do con người chấm.
- [ ] Kết quả eval lưu prompt version, model version và config.
- [ ] Mỗi request có `trace_id`, mỗi node có `span_id`.
- [ ] Trace nối được route, retrieval, tool, handoff, retry và approval.
- [ ] Thu success/error rate, p50/p95 latency, token, cost và tool error rate.
- [ ] Log được redact trước khi lưu.
- [ ] Có failure taxonomy cho model, retrieval, tool, routing và policy.

### Kiểm chứng

- [ ] Có một lệnh chạy toàn bộ eval và xuất report.
- [ ] Eval lặp nhiều lần với case không deterministic và báo mean/pass rate.
- [ ] Quality gate chặn được một phiên bản cố tình làm giảm chất lượng.
- [ ] Một trace bất kỳ cho phép lần lại toàn bộ workflow.
- [ ] Mọi run tính được tổng latency, token và cost.
- [ ] Không có API key hoặc PII giả lập trong log.

### Bắt buộc để qua tuần

- [ ] Regression suite đạt quality gate đã chốt.
- [ ] Eval report có thể so sánh ít nhất hai phiên bản.
- [ ] Có đủ dữ liệu để xác định lỗi nằm ở model, retrieval, tool, routing hay policy.

---

## Tuần 6 — Tối ưu và triển khai

### Hiểu

- [ ] Giải thích được streaming, concurrency, timeout và backpressure.
- [ ] Giải thích được cache invalidation và rủi ro dữ liệu cũ.
- [ ] Hiểu model routing theo độ khó.
- [ ] Phân biệt stateless API với persistent workflow state.
- [ ] Hiểu token/cost budget và cơ chế degrade an toàn.

### Làm được

- [ ] Hoàn thiện `/v1/chat`, stream, xem run, approve, ingest, health và ready endpoints.
- [ ] Stream event có schema cho status, partial answer, citation, approval và error.
- [ ] Có authentication tối thiểu và rate limiting.
- [ ] Cache embedding/retrieval có TTL hoặc quy tắc invalidation rõ ràng.
- [ ] Model nhỏ xử lý task đơn giản; model mạnh chỉ dùng khi cần.
- [ ] Worker chạy song song nhưng có giới hạn concurrency.
- [ ] Mỗi run có token/cost budget và hành vi khi vượt budget.
- [ ] Ứng dụng được container hóa với config dev/prod tách biệt.
- [ ] Có graceful shutdown và load test cơ bản.
- [ ] Có runbook cho deploy, rollback, rotate key, re-index và sự cố.
- [ ] Có UI hoặc demo client thể hiện toàn bộ luồng chính.

### Kiểm chứng

- [ ] Direct chat, RAG, multi-agent, review và approval chạy end-to-end.
- [ ] p95 latency và chi phí nằm trong SLO tự đặt.
- [ ] Load test đạt concurrency mục tiêu mà không mất state.
- [ ] Container mới có thể khởi động chỉ bằng hướng dẫn trong README.
- [ ] Thử rollback thành công.
- [ ] Chạy lại full eval sau deployment và vẫn đạt quality gate.

### Bắt buộc để hoàn thành project

- [ ] Tất cả use case P0 chạy end-to-end.
- [ ] Tất cả thuật ngữ trong ma trận `Plan2.md` có code, test hoặc artifact làm bằng chứng.
- [ ] Không còn lỗi safety nghiêm trọng đã biết.
- [ ] API, UI demo, architecture docs, threat model và runbook đều đầy đủ.
- [ ] Một developer khác có thể clone, cấu hình, ingest và chạy demo chỉ bằng README.

---

## Nhật ký tổng kết mỗi tuần

Sao chép mẫu này sau mỗi tuần:

```text
Tuần:
Ngày hoàn thành:

Tôi tự xây được:
-

Tôi có thể tự giải thích:
-

Test/metric đạt được:
-

Lỗi khó nhất và cách sửa:
-

Điểm còn yếu:
-

Artifact minh chứng (file, test report, trace, screenshot):
-

Quyết định: [ ] Qua tuần  [ ] Học/làm lại phần còn thiếu
```
